import argparse
import io
import os
import speech_recognition as sr
import whisper
import torch

from datetime import datetime
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform

from pygame import mixer
from gtts import gTTS
import time

if os.name == "posix":
    from pydub import AudioSegment

import json
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage  # noqa: F401
from typing import List

model = OllamaFunctions(model="llama3:70b", base_url='http://172.28.105.30/backend', format='json')

# define function structure in pydantic

class Solution(BaseModel):
    temperature: float = Field(
        ..., description="The temperature of the solution creation")
    atmosphere: str = Field(
        ..., description="The atmosphere of the solution creation")
    method: str = Field(
        ..., description="The method of the solution creation")
    time: float = Field(
        ..., description="The time needed for the solution creation")
    solutes: List[str] = Field(
        ..., description="The solutes used in the solution")
    solute_masses: List[float] = Field(
        ..., description="The masses in miligramm of the solutes used in the solution")
    solvents: List[str] = Field(
        ..., description="The solvents used in the solution")
    solvent_volumes: List[float] = Field(
        ..., description="The volumes in mililiter of the solvents used in the solution")
    
class Scaling(BaseModel):
    powder: str = Field(
        ..., description="The name of the powder to be scaled")
    mass: float = Field(
        ..., description="The scaled mass of the powder in milligrams")

prompt = PromptTemplate.from_template(
    """
You should extract the information from the following text and create a structured output.
If information is missing you should fill it with null.
If something is unclear you should ask for clarification.

Human: {question}
AI:
"""
)

model = model.bind_tools(
    tools=[
        {
            "name": "SolutionPreparation",
            "description": "Schema for solution preparation",
            "parameters": Solution.schema(),
        },
        {
            "name": "PowderScaling",
            "description": "Schema for powder scaling",
            "parameters": Scaling.schema(),
        }
    ],
)

chain = prompt | model

# PART 1

def say(text, filename="temp.mp3", delete_audio_file=True, language="en", slow=False):
    # PART 2
    audio = gTTS(text, lang=language, slow=slow)
    audio.save(filename)

    if os.name == "posix":
        sound = AudioSegment.from_mp3(filename)
        old_filename = filename
        filename = filename.split(".")[0] + ".ogg"
        sound.export(filename, format="ogg")
        if delete_audio_file:
            os.remove(old_filename)

    # PART 3
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    # PART 4
    seconds = 0
    while mixer.music.get_busy() == 1:
        time.sleep(0.25)
        seconds += 0.25

    # PART 5
    mixer.quit()
    if delete_audio_file:
        os.remove(filename)
    print(f"audio file played for {seconds} seconds")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="small", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=2,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    recorder.pause_threshold = 2
    # Important for linux users.
    # Prevents permanent application hang and crash by using the wrong Microphone
    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000)

    # Load / Download model
    model = args.model
    if args.model != "large" and not args.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model)

    phrase_timeout = args.phrase_timeout

    temp_file = NamedTemporaryFile().name

    # with source:
    #     recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    # recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Model loaded.\n")
    messages = []
    messages.append(
        {"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    print(phrase_timeout)
    while True:
        try:
            with source:
                audio = recorder.listen(source)

            # Use AudioData to convert the raw data to wav data.
            wav_data = io.BytesIO(audio.get_wav_data())

            # Write wav data to the temporary file as bytes.
            with open(temp_file, 'w+b') as f:
                f.write(wav_data.read())

            # Read the transcription.
            result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
            text = result['text'].strip()

            # If we detected a pause between recordings, add a new item to our transcription.
            # Otherwise edit the existing one.
            if text.lower().startswith("stop"):
                break
            print(text)
            # messages.append({"role": "user", "content": text})
            # print(messages)
            chat_response = chain.invoke(text)
            assistant_message = chat_response #.json()["choices"][0]["message"]  # Attempt to Port to new API 
            print(assistant_message)
            messages.append(assistant_message)
            # if assistant_message["content"]:
            #     say(assistant_message["content"])
            if "function_call" in assistant_message.additional_kwargs:
                say("The assistant is happy, if you want it to repeat or ask if something is missing, please say so.")
                res = json.loads(assistant_message.additional_kwargs["function_call"]["arguments"])
                schema = assistant_message.additional_kwargs["function_call"]["name"]
                res["m_def"] = "../upload/raw/nomad_schema.archive.yaml#"+schema
                filename = "nomad_entry_"+schema+".archive.json"
                with open(filename, "w") as outfile:
                    json.dump({"data": res}, outfile, indent=2)

            # Clear the console to reprint the updated transcription.
            os.system('cls' if os.name == 'nt' else 'clear')

            # Infinite loops are bad for processors, must sleep.

            sleep(0.25)
        except KeyboardInterrupt:
            break


main()
