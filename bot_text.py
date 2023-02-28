from json import load
from typing import Dict


def read_text_information() -> Dict[str, str]:
    """
    Read a JSON file with text information and return a dictionary with the contents.

    Parameters:
    None

    Returns:
    Dict[str, str]: A dictionary with the contents of the JSON file.
    """
    with open('texts.json', 'r', encoding='utf-8') as file:
        text: Dict[str, str] = load(file)
    return text


texts: Dict[str, str] = read_text_information()
