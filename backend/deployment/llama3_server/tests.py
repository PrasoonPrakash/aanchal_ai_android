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


if __name__ == '__main__':
    audio_file = './audio_1723623102704.wav'
    print(transcribe(audio_file))

    # audio_file = './hi-question.webm'
    # print(transcribe(audio_file))

##########################
# import librosa
# import torch
# from transformers import WhisperProcessor, WhisperForConditionalGeneration

# # Load the Whisper processor and model from Hugging Face
# model_name = "openai/whisper-large"
# processor = WhisperProcessor.from_pretrained(model_name)
# model = WhisperForConditionalGeneration.from_pretrained(model_name)
# model = model.to('cuda')
# forced_decoder_ids = processor.get_decoder_prompt_ids(language="hindi", task="transcribe")


# # Load the audio file using librosa
# audio_path = './audio_1723623102704.wav'  # Replace with your audio file path
# audio, sr = librosa.load(audio_path, sr=16000)  # Load with 16kHz sample rate

# # Preprocess the audio (convert to model's input format)
# input_features = processor(audio, sampling_rate=sr, return_tensors="pt").input_features.to('cuda')

# # Perform transcription
# with torch.no_grad():
#     predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)

# # Decode the transcription
# transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

# print("Transcription:", transcription)
