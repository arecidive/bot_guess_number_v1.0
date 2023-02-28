from json import decoder, load, dump
from typing import Union, Dict, List


def check_json_file(file_name: str) -> Union[Dict, Dict[str, Dict[str, Union[int, bool]]]]:
    """
    Check if the JSON file exists and has a valid format. Return an empty
    dictionary if the file is empty or has an invalid format.

    Parameters:
    file_name (str): The name of the JSON file.

    Returns:
    Union[Dict, Dict[str, Dict[str, Union[int, bool]]]]: The content of the JSON
    file if it has a valid format, or an empty dictionary if the file is empty or has an invalid format.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return load(f)
    except decoder.JSONDecodeError:
        return {}


def write_stats(stat: Dict[str, Dict[str, Union[int, bool]]]) -> None:
    """
    Write a dictionary with user statistics to a JSON file.

    Parameters:
    stat (Dict[str, Dict[str, Union[int, bool]]]): A dictionary containing user statistics.

    Returns:
    None
    """
    with open('stats.json', 'w', encoding='utf-8') as file_users:
        dump(stat, file_users, indent=4)


user: Dict[str, Union[int, bool]] = {
    'game': False,
    'number_attempts': 0,
    'number_wins': 0,
    'number_games': 0,
    'random_number': 0
}

users: Dict[str, Dict[str, Union[int, bool]]] = check_json_file('stats.json')
users_top: List = []
