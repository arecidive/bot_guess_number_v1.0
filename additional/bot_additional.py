from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command, Text
from random import randint
from typing import Tuple
from requests import get, Response
from additional.bot_text import texts
from users.bot_info_about_user import *


def cats_photos() -> str:
    """
    This function sends a request to the API of https://aws.random.cat/ and returns
    the URL of a random image of a cat from the response in JSON format. If the
    request fails, it returns the value of the texts['static_address'] key.

    Parameters: None

    Returns: str: a URL of a random cat image or texts['static_address'].
    """
    API_CATS_URL: str = 'https://aws.random.cat/meow'
    cat_response: Response = get(API_CATS_URL)
    if cat_response.status_code == 200:
        return cat_response.json()['file']
    return texts['static_address']


def tops(list_users: List) -> str:
    """
    This function takes a list of tuples that contains the usernames and their number
    of wins, and returns a string that represents the top three users with the most wins
    sorted by their wins and then by their usernames in alphabetical order. If there are no
    winners or the list is empty, it returns a message that there are no winners.

    Parameters: list_users (List): A list of tuples that contains the usernames
    and their number of wins.

    Returns: str: a string that represents the top three users with the most wins
    sorted by their wins and then by their usernames in alphabetical order
    or a message that there are no winners.
    """
    for username in users.keys():
        cur_user: Tuple[str, int] = (f'@{username}', users[username]['number_wins'])
        if users[username]['number_wins'] and cur_user not in list_users:
            list_users.extend([cur_user])
    time_list_users: List[(str, int)] = sorted(list_users, key=lambda us: (us[1], us[0]), reverse=True)[:3]
    if time_list_users:
        for numb, elem in enumerate(time_list_users):
            time_list_users[numb]: str = texts['text_top_prize'].format(
                m=numb + 1, name=time_list_users[numb][0], cnt=time_list_users[numb][1]
            )
        return texts['text_users_top_prize'].format(top_users='\n'.join(time_list_users))
    return texts['text_lack_prizes']
