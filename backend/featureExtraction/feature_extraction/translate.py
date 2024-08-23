from .prompter import prompter


def translate(text):
    messages = [
        {'role': 'user', 'content': 'Translate the following Hindi text to English. Just output the translation and not the input itself.' + text}
    ]
    ret = prompter(messages, max_new_tokens=1024)
    return ret
