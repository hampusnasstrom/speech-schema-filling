import os
import sys
import datetime
import argparse

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper

from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage

model = Ollama(model="llama3:70b", base_url='http://172.28.105.30/backend')


def transcribe(audio_file):
    #transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    # model = args.model
    # if args.model != "large" and not args.non_english:
    #     model = model + ".en"
    audio_model = whisper.load_model(model)
    transcript = audio_model.transcribe(audio_file, fp16=torch.cuda.is_available())
    
    return transcript

def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name


def transcribe_audio(file_path):
    """
    Transcribe the audio file at the specified path.

    :param file_path: The path of the audio file to transcribe
    :return: The transcribed text
    """
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)

    return transcript["text"]

def main():
    st.title("speech 2 schema")
    
    tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

    with tab1:
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            save_audio_file(audio_bytes, "mp3")

    with tab2:
        audio_file = st.file_uploader("Upload Audiofile", type=["mp3", "mp4", "wav", "m4a"])
        if audio_file:
            file_extension = audio_file.type.split('/')[1]
            save_audio_file(audio_file.read(), file_extension)
    
    if st.button("Transcribe"):
        # Find the newest audio file
        audio_file_path = max(
            [f for f in os.listdir(".") if f.startswith("audio")],
            key=os.path.getctime,
        )

        # Transcribe the audio file
        transcript_text = transcribe_audio(audio_file_path)

        # Display the transcript
        st.header("Transcript")
        st.write(transcript_text)

        # Save the transcript to a text file
        with open("transcript.txt", "w") as f:
            f.write(transcript_text)

        # Provide a download button for the transcript
        st.download_button("Download Transcript", transcript_text)


if __name__ == "__main__":
    # Set up the working directory
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)

    # Run the main function
    main()