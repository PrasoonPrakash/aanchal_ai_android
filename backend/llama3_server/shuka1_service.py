# SET export NO_PROXY=localhost,127.0.0.1

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from fastapi import FastAPI
from pydantic import BaseModel
import torch
import librosa
from typing import List

DEVICE = 'cuda'
assert torch.cuda.is_available(), "CUDA not available"

# Initialize FastAPI
app = FastAPI()

# Load the model and tokenizer
pipe = pipeline(
    model='sarvamai/shuka_v1', trust_remote_code=True, device=DEVICE,
    torch_dtype=torch.bfloat16
)
print('Model loaded successfully')


class TranscriptionInput(BaseModel):
    audio_file: str = 'dummy.mp4'
    sampling_rate: int = 16000


INSTRUCTIONS = """Given an audio containing a Hindi doctor-patient conversation. Transcribe the audio into hindi text. Make sure you adhere to the following instructions.
1. Ignore background noise from the audio.
2. Identify the doctor and patient speech.
3. Output must be in Devnagari script.
4. Add punctuations whenever possible.
5. Perform speaker diarization, i.e., add "Doctor:" and "Patient:" prefixes to doctor and patient speeches respectively."""

def get_transcription(audio_file, sampling_rate):
    audio, sr = librosa.load(audio_file, sr=16000)
    turns = [
        {'role': 'system', 'content': INSTRUCTIONS},
        {'role': 'user', 'content': '<|audio|>'}
    ]

    print(audio.shape)
    generated_text = pipe({'audio': audio, 'turns': turns, 'sampling_rate': sr}, max_new_tokens=1024)
    print(generated_text)
    
    return generated_text


@app.post("/transcribe/")
def generate_text(input: TranscriptionInput):
    # Concatenate messages
    try:
        generated_text = get_transcription(input.audio_file, input.sampling_rate)
    except Exception as e:
        print('Following error occured during execution of the model\n' + str(e))
        generated_text = 'ERROR!'

    return {"output": generated_text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)
