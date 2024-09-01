import requests
import json
import os

os.environ['NO_PROXY'] = "localhost,127.0.0.1"

# llama3_url = "http://localhost:8000/generate/"
service_endopoint = os.environ.get('LLAMA3_SERVICE', 'http://localhost:8000')
llama3_url = f"{service_endopoint}/generate/"
def prompter(messages, max_new_tokens=512, temperature=None):
    data = {
        "messages": messages,
        "max_new_tokens": max_new_tokens,
    }
    if temperature is not None:
        data['temperature'] = temperature

    response = requests.post(llama3_url, json=data)

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
