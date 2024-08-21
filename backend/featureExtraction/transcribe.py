import assemblyai as aai

aai.settings.api_key = "e7965528d42e418fa3e74b523b235ee2"
audio_url = "/home/prasoon/breast_cancer_project/trial1/featureExtraction/uploads/Ptcode905control.mp4"
#print(file_path)
config = aai.TranscriptionConfig(language_code='hi')
#print(config)
transcriber = aai.Transcriber(config=config)
#print(transcriber)
transcript = transcriber.transcribe(audio_url)
#print(transcript)
hindiPath="/home/prasoon/breast_cancer_project/trial1/featureExtraction/hindiTranscripts/Ptcode905control_hindi.txt"
#print(hindiPath)
#print(name)
f1=open(hindiPath,'w')
#prediction = model.predict(audio_url)
text=transcript.text
f1.write(text)
#print(text)
print("uploaded")
#return hindiPath