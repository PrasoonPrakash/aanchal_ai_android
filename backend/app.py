from flask import Flask, request, jsonify
import os
#import ffmpeg
import assemblyai as aai
#from config import assemblyai_key
#import pickle
import pandas as pd
import numpy as np
#from prompter import OpenAIPrompter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#with open("randomForest.pkl","rb") as f:
 #   model=pickle.load(f)
 
"""model="gpt-35-turbo"
prompter = OpenAIPrompter(model, max_tokens=16)

feat_ids = [
      "AGE", "MARITAL STATUS", "MARRIAGE_DURATION",
      "EDUCATION", "OCCUPATION", "FAMILY TYPE", "RELIGION",
     # Medical
     # "PAST_SURGERY", # --> Missing
      "MENSTRUAL_STATUS",
      "TYPE OF MENOPAUSE(NATURAL/HYSTERECTOMY)", "PHYSICAL ACTIVITY",
      "ABORTION",
     "ABORTION_NO.",
]"""

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    #file_name=file.filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"Is patient at risk of breast cancer?": process_CSV_file(file_path)}), 200

def process_CSV_file(file_path):
    try:
        aai.settings.api_key = "42906185b53b4fb180376d15b40d8f06"
        audio_url = file_path
        #print(file_path)
        config = aai.TranscriptionConfig(language_code='hi')
        #print(config)
        transcriber = aai.Transcriber(config=config)
        #print(transcriber)
        transcript = transcriber.transcribe(audio_url)
        #print(transcript)
        f1=open("transcription.txt",'w')
        #prediction = model.predict(audio_url)
        f1.write(transcript.text)
        text=transcript.text
        #print(text)
        return transcript.text
    except:
        return "an exception occurred"
        
#def featureExtraction(engText_path)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)


