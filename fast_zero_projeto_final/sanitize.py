import bleach
import re


def sanitize_script(text: str):
    return bleach.clean(text, strip=True)


def sanitize_spaces(text: str):
    no_script: str = sanitize_script(text)
    split: list[str] = no_script.split(' ')
    filtered: list[str] = filter(lambda char: char, split)
    return ' '.join(filtered)


def sanitize_punctuation(text: str):
    return re.sub(r'[^\w\s]', '', text)


def sanitize_case(text: str):
    return text.lower()


def sanitize_nome(nome: str):
    no_script = sanitize_script(nome)
    no_punctuation = sanitize_punctuation(no_script)
    no_space = sanitize_spaces(no_punctuation)
    no_case = sanitize_case(no_space)
    return no_case
