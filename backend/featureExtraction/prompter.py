from typing import Any
import openai
from time import sleep
import os
#from .env import OPENAI_ENDPOINT
#from .env import OPENAI_KEY


class OpenAIPrompter:
    def __init__(self, model, max_tokens=8) -> None:
        self.client = openai.OpenAI(
            base_url=os.environ['OPENAI_ENDPOINT'], 
            api_key=os.environ['OPENAI_KEY'],
            #api_version="2024-02-01"
        )
        self.model = model
        self.max_tokens = max_tokens

    def __call__(self, prompt_elems) -> Any:
        backoff = 5
        succeeded = False
        max_tries = 5
        succeeded = False
        while not succeeded:
            try:
                ret = self.client.chat.completions.create(
                    model=self.model, #engine=model,
                    messages=prompt_elems,
                    max_tokens=self.max_tokens,
                    # stop=STOP,
                    temperature=0.0,
                    top_p=0.0,
                    n=1,
                    seed=42
                )
                succeeded = True
            except Exception as e:
                print(e)
                max_tries -= 1
                print(f'Sleeping for {backoff}s')
                sleep(backoff)
                backoff += 10
                if max_tries == 0:
                    break

        if not succeeded:
            return None

        return ret.choices[0].message.content
