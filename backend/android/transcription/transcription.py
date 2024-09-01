import requests
import json
import os

os.environ['NO_PROXY'] = "localhost,127.0.0.1"

service_endopoint = os.environ.get('LLAMA3_SERVICE', 'http://localhost:8000')

# transcription_url = "http://localhost:8080/transcribe/"

def transcribe(audio_file):
    transcription_url = f"{service_endopoint}/transcribe/"
    
    data = {"audio_file": audio_file}
    response = requests.post(transcription_url, json=data)

    # Check the status code
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        if result["output"] == "ERROR!":
            print("There was an error at the server side")

        return result["output"]

    print("Failed to get a response. Status code:", response.status_code)
    print("Response content:", response.text)

    return "ERROR!"


def transcribe2(audio_file):
    transcription_url = f"{service_endopoint}/transcribe2/"

    with open(audio_file, "rb") as f:
        files = {"file": (audio_file, f, "audio/mpeg")}
        response = requests.post(transcription_url, files=files)

    # Check the status code
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        if result["output"] == "ERROR!":
            print("There was an error at the server side")

        return result["output"]

    print("Failed to get a response. Status code:", response.status_code)
    print("Response content:", response.text)

    return "ERROR!"
