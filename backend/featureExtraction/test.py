import os
import sys
import openai
from prompter import OpenAIPrompter
from punc import INSTRUCTIONS

# Ensure the environment variables for OpenAI API are set
#assert 'OPENAI_KEY' in os.environ, "Please set the OpenAI API key in the environment variables."

# Initialize the OpenAIPrompter
model="gpt-3.5-turbo-0125"
prompter = OpenAIPrompter(model,max_tokens=500)

# Read the Hindi text from the file
file_path = sys.argv[1]
with open(file_path, 'r', encoding='utf-8') as f:
    hindi_text = f.read()

def get_zero_shot_prompt(hindi_text):
    prompt_elems = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": hindi_text}
    ]
    return prompt_elems

if __name__ == "__main__":
    try:
        # Prepare the prompt
        prompt = get_zero_shot_prompt(hindi_text)
        
        # Call the OpenAI API to get the response
        response = prompter(prompt)
        write_path="tmp.txt"
        if response:
            # Write the response back to the original file
            with open(write_path, 'w', encoding='utf-8') as f:
                f.write(response)
        else:
            print("Failed to get a response from the OpenAI API.")
    except Exception as e:
        print(f"An error occurred: {e}")

