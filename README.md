# LLM Hackathon for Materials and Chemistry 2024 - Audio Documentation and ELN Structured Data Entry

<p align="center">
  <img src="https://github.com/hampusnasstrom/speech-schema-filling/assets/64071335/e28e1156-ac53-4212-bc1a-d211106211b9">
</p>
This repository contains a solution for the LLM Hackathon for Materials and Chemistry 2024. The project aims to facilitate the documentation of lab experiments using audio and structured data entries in an Electronic Lab Notebook (ELN) based on the NOMAD schema.

## Overview

The solution uses speech recognition to transcribe audio recordings of lab experiments into text. The transcribed text is then processed and structured according to json-schema, and then written into an ELN entry in NOMAD. This allows for efficient and hands-free documentation of lab experiments.

## Key Components

- **Speech Recognition**: The [`speech_to_instance.py`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/speech_to_instance.py) script uses the `speech_recognition` and `whisper` libraries to transcribe audio into text. The audio is captured using a microphone, and the transcription is done in real-time.

- **Text Processing and Structuring**: The transcribed text is processed and structured according to the NOMAD schema defined in [`nomad_schema.archive.yaml`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/nomad_schema.archive.yaml). The [`create_solution_entry`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/speech_to_instance.py#L31) function is used to create structured data entries for NOMAD.

- **ELN Entry**: The structured data is written into an ELN as a JSON file. This is done in the `main` function.

## Usage

To run the script, use the following command:

```sh
python speech_to_instance.py
```

The script will start recording audio and transcribing it into text. It will then process the text and write structured data entries into an ELN.

## Dependencies

The project depends on several Python libraries, including [`speech_recognition`](https://github.com/Uberi/speech_recognition#readme), [`whisper`](https://github.com/openai/whisper), `pygame`, `gtts`, and `pydub`. These can be installed using the requirements file:

```sh
pip install -r requirements.txt
```

## Conclusion

This solution provides a hands-free and efficient way to document lab experiments and write structured data entries into an ELN. It is particularly useful for labs where manual documentation can be cumbersome or impractical because scientists might need both hands in the glovebox while experimenting. The use of a local instance of an LLM is very important, as these experiments protect the IP of the scientist. In this implementation, we used the Llama3:70b model served via Ollama protecting the privacy and still offering an efficient solution for the text processing and structuring (via function calling).
