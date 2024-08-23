import requests
import json
import os

os.environ['NO_PROXY'] = "localhost,127.0.0.1"

# transcription_url = "http://localhost:8080/transcribe/"
transcription_url = "http://localhost:8000/transcribe/"
def transcribe(audio_file):
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
