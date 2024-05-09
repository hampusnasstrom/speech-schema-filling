# Speech to ELN Structured Data Entry

<p align="center">
  <img src="https://github.com/hampusnasstrom/speech-schema-filling/assets/64071335/e28e1156-ac53-4212-bc1a-d211106211b9">
</p>
This repository contains a solution for the LLM Hackathon for Materials and Chemistry 2024. The project aims to facilitate the documentation of lab experiments using audio and structured data entries in an Electronic Lab Notebook (ELN) based on the NOMAD schema.

## Overview
 [![NOMAD](https://img.shields.io/badge/Open%20NOMAD-lightgray?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDI3LjUuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCAxNTAwIDE1MDAiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDE1MDAgMTUwMDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8c3R5bGUgdHlwZT0idGV4dC9jc3MiPgoJLnN0MHtmaWxsOiMxOTJFODY7c3Ryb2tlOiMxOTJFODY7c3Ryb2tlLXdpZHRoOjE0MS4zMjI3O3N0cm9rZS1taXRlcmxpbWl0OjEwO30KCS5zdDF7ZmlsbDojMkE0Q0RGO3N0cm9rZTojMkE0Q0RGO3N0cm9rZS13aWR0aDoxNDEuMzIyNztzdHJva2UtbWl0ZXJsaW1pdDoxMDt9Cjwvc3R5bGU+CjxwYXRoIGNsYXNzPSJzdDAiIGQ9Ik0xMTM2LjQsNjM2LjVjMTUwLjgsMCwyNzMuMS0xMjEuOSwyNzMuMS0yNzIuMlMxMjg3LjIsOTIuMSwxMTM2LjQsOTIuMWMtMTUwLjgsMC0yNzMuMSwxMjEuOS0yNzMuMSwyNzIuMgoJUzk4NS42LDYzNi41LDExMzYuNCw2MzYuNXoiLz4KPHBhdGggY2xhc3M9InN0MSIgZD0iTTEzMjksOTQ2Yy0xMDYuNC0xMDYtMjc4LjgtMTA2LTM4Ni4xLDBjLTk5LjYsOTkuMy0yNTguNywxMDYtMzY1LjEsMTguMWMtNi43LTcuNi0xMy40LTE2LjItMjEuMS0yMy45CgljLTEwNi40LTEwNi0xMDYuNC0yNzgsMC0zODQuOWMxMDYuNC0xMDYsMTA2LjQtMjc4LDAtMzg0LjlzLTI3OC44LTEwNi0zODYuMSwwYy0xMDcuMywxMDYtMTA2LjQsMjc4LDAsMzg0LjkKCWMxMDYuNCwxMDYsMTA2LjQsMjc4LDAsMzg0LjljLTYzLjIsNjMtODkuMSwxNTAtNzYuNywyMzIuMWM3LjcsNTcuMywzMy41LDExMy43LDc3LjYsMTU3LjZjMTA2LjQsMTA2LDI3OC44LDEwNiwzODYuMSwwCgljMTA2LjQtMTA2LDI3OC44LTEwNiwzODYuMSwwYzEwNi40LDEwNiwyNzguOCwxMDYsMzg2LjEsMEMxNDM1LjQsMTIyNCwxNDM1LjQsMTA1MiwxMzI5LDk0NnoiLz4KPC9zdmc+Cg==)](https://nomad-lab.eu/nomad-lab/)

The solution uses speech recognition to transcribe audio recordings of lab experiments into text. The transcribed text is then processed and structured according to [JSON schema](https://json-schema.org/), and then written into an ELN entry in [NOMAD](https://nomad-lab.eu/nomad-lab/). This allows for efficient and hands-free documentation of lab experiments.

## Key Components

- **Speech Recognition**: The [`speech_to_instance.py`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/speech_to_instance.py) script uses the [`speech_recognition`](https://github.com/Uberi/speech_recognition#readme) and [`whisper`](https://github.com/openai/whisper) libraries to transcribe audio into text. The audio is captured using a microphone, and the transcription is done in real-time.

- **Text Processing and Structuring**: The transcribed text is processed and structured according to the NOMAD schema defined in [`nomad_schema.archive.yaml`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/nomad_schema.archive.yaml). The [`create_solution_entry`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/speech_to_instance.py#L31) function is used to create structured data entries for NOMAD.

- **ELN Entry**: The structured data is written into an ELN as a JSON file. This is done in the `main` function.

## Usage

To run the script, use the following command:

```sh
python speech_to_instance.py
```

The script will start recording audio and transcribing it into text. It will then process the text and write structured data entries into an ELN.

An example notebook demonstrating the conversion from the extracted text from the audio to a structured [JSON schema](https://json-schema.org/) is available in the [`text_to_instance.ipynb`](https://github.com/hampusnasstrom/speech-schema-filling/blob/main/text_to_instance.ipynb).

## Dependencies

The project depends on several Python libraries, including [`speech_recognition`](https://github.com/Uberi/speech_recognition#readme), [`whisper`](https://github.com/openai/whisper), [`langchain`](https://github.com/langchain-ai/langchain),  [`pygame`](https://github.com/pygame/pygame), `gtts`, and [`pydub`](https://github.com/jiaaro/pydub). It is recommended to create a virtual environment first. Then the dependencies can be installed using the requirements file:

```sh
pip install -r requirements.txt
```

Additionally make sure you have ffmpeg installed.

## Conclusion

This solution provides a hands-free and efficient way to document lab experiments and write structured data entries into an ELN. It is particularly useful for labs where manual documentation can be cumbersome or impractical because scientists might need both hands in the glovebox while experimenting. The use of a local instance of an LLM is very important, as these experiments protect the IP of the scientist. In this implementation, we used the Llama3:70b model served via Ollama protecting the privacy and still offering an efficient solution for the text processing and structuring (via function calling).
