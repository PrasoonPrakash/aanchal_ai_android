from .prompter import prompter


TRANSLATION_INSTRUCTIONS = """
Translate the following Hindi text to English.

INSTRUCTIONS:
1. Input Hindi text may not contain any punctuations. Try to add punctuations if needed.
2. The output must be in English with punctuations.
3. Just output an English translation not the input.
5. Your answer must be in the following format. Answer: <translated-text>.

Here is the Hindi text.
"""

# 'Translate the following Hindi text to English. Just output the translation and not the input itself. Make sure the output is in English.'
def translate(text):
    messages = [
        {'role': 'user', 'content': TRANSLATION_INSTRUCTIONS + text}
    ]
    ret = prompter(messages, max_new_tokens=1024)
    ret = ret.split('Answer:')[-1].lstrip()

    return ret
