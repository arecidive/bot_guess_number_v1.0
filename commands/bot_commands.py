from additional.bot_additional import *

API_BOT: str = ''
bot: Bot = Bot(token=API_BOT)
dispatcher: Dispatcher = Dispatcher()


@dispatcher.message(Command(commands=['start']))
async def handle_start_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Handler function for the /start command.
    The function checks if the user who sent the message is registered in the user's
    dictionary. If not, a new entry with the user's username is added to the dictionary, using a copy
    of the user dictionary as the default values. If the user is not currently playing a game, the
    function sends a welcome message with a photo of a cat and instructions on how to start a new game.
    The caption of the photo is generated using the texts['text_start'] string, which takes the user's
    first name, the list of approval answers, and the list of rejection answers as parameters. If the user
    is currently playing a game, the function sends a message indicating that the user needs to input a
    number to continue the game. The caption of the photo is generated using the texts['text_not_digit'] string.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.
    """
    username: str = message.from_user.username
    if username not in users:
        users[username] = user.copy()
    write_stats(users)
    if not users[username]['game']:
        await message.answer_photo(photo=cats_photos(), caption=texts['text_start'].format(
            name=message.from_user.first_name,
            approval=' '.join(texts['user_answers_approval']),
            rejection=' '.join(texts['user_answers_rejection'])
            )
        )
    else:
        await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])


@dispatcher.message(Command(commands=['help']))
async def handle_help_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Handler function for the /help command.
    The function checks whether the username of the message sender is in the
    user's dictionary. If it is, the function sends a photo and a caption with the
    text from the texts dictionary that corresponds to the 'text_help' key. If the
    username is not in the user's dictionary, the function sends a photo and a caption
    with the text from the texts dictionary that corresponds to the 'registration_requirement_text' key.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.
    """
    username: str = message.from_user.username
    if username in users:
        await message.answer_photo(photo=cats_photos(), caption=texts['text_help'])
    else:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(Command(commands=['stat']))
async def handle_stat_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Handler function for the /stat command.
    Handler  sends a photo with a caption containing statistics about the user's games and prizes won
    if the user is already registered in the database and is not currently playing a game. If the user is
    currently playing a game, a message is sent instructing them to input only numbers. If the user is
    not registered yet, a message is sent instructing them to register first.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.
    """
    try:
        username: str = message.from_user.username
        if not users[username]['game']:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_stat'].format(
                cnt_games=users[username]["number_games"],
                cnt_prizes=users[username]["number_wins"]
                )
            )
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])
    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(Command(commands=['cancel']))
async def handle_cancel_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Handler function for the /cancel command.
    Function cancels the game for the user if they were playing. A message is sent
    confirming the game is over. If the user is not playing a game, a message is sent
    indicating that they cannot cancel. If the user is not registered yet, a message is
    sent instructing them to register first.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.
    """
    username: str = message.from_user.username
    try:
        if users[username]['game']:
            users[username]['game'] = False
            await message.answer_photo(photo=cats_photos(), caption=texts['text_end_game'].format(
                approval=' '.join(texts['user_answers_approval'])
                )
            )
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_cancel'])
        write_stats(users)
    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(Command(commands=['top']))
async def handle_top_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Sends the leaderboard of the top players to the user who sent the command.
    This function is called when the user sends the /top command to the bot. The function checks
    whether the user has already registered with the bot, and if they have not, it sends a
    registration requirement message. If the user is registered and not currently playing a game, it
    sends a message with the current leaderboard of top players. If the user is playing a game, it
    sends a message indicating that the leaderboard is not available during gameplay.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.
    """
    username: str = message.from_user.username
    if username in users:
        if not users[username]['game']:
            await message.answer_photo(photo=cats_photos(), caption=tops(users_top))
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])
    else:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(Text(text=texts['user_answers_approval'], ignore_case=True))
async def handle_approval_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    This function handles a message from a user indicating their approval to start a game.
    It checks if the user is registered and not already in a game. If both conditions are met,
    it initializes a game for the user with a random number to guess.
    If the user is not registered, a KeyError is raised.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.

    Raises:
    KeyError: If the user is not registered.
    """
    username: str = message.from_user.username
    try:
        if not users[username]['game']:
            users[username]['game'] = True
            users[username]['number_attempts'] = 5
            users[username]['random_number'] = randint(1, 100)
            await message.answer_photo(photo=cats_photos(), caption=texts['text_approval_game'])
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])
        write_stats(users)
    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(Text(text=texts['user_answers_rejection'], ignore_case=True))
async def handle_rejection_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    Handles rejection messages from the user.
    If the user is not registered or not currently in a game, a photo and
    caption are sent with a rejection message. Otherwise, a photo and caption are sent
    indicating that the user did not enter a number.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.

    Raises:
    KeyError: If the user is not registered.
    """
    username: str = message.from_user.username
    try:
        if not users[username]['game']:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_rejection_game'].format(
                approval=' '.join(texts['user_answers_approval'])
                )
            )
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])
    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message(lambda num: num.text and num.text.isdigit())
async def handle_digit_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    This function handles messages from users that contain a digit. It checks if the user is playing the game
    and then compares the number entered by the user to the random number generated for the user. The function
    sends appropriate messages to the user based on whether the number entered is correct, too high, or too low.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.

    Raises:
    KeyError: If the user is not registered.
    """
    username: str = message.from_user.username
    number: int = int(message.text)
    try:

        if users[username]['game']:

            if number == users[username]['random_number']:
                users[username]['game'] = False
                users[username]['number_games'] += 1
                users[username]['number_wins'] += 1
                await message.answer_photo(photo=cats_photos(), caption=texts['text_number_is_number'].format(
                        number=users[username]['random_number'], approval=' '.join(texts['user_answers_approval'])
                    )
                )

            elif number > users[username]['random_number']:
                users[username]['number_attempts'] -= 1
                await message.answer_photo(photo=cats_photos(), caption=texts['text_number_is_small'].format(
                        cnt=users[username]['number_attempts']
                    )
                )

            else:
                users[username]['number_attempts'] -= 1
                await message.answer_photo(photo=cats_photos(), caption=texts['text_number_is_big'].format(
                    cnt=users[username]['number_attempts']
                    )
                )

            if users[username]['number_attempts'] == 0:
                users[username]['game'] = False
                users[username]['number_games'] += 1
                await message.answer_photo(photo=cats_photos(), caption=texts['text_null_attempts'].format(
                        number=users[username]['random_number'], approval=' '.join(texts['user_answers_approval'])
                    )
                )

        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_command'])
        write_stats(users)

    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])


@dispatcher.message()
async def handle_all_message(message: Message) -> 'aiogram.methods.send_photo.SendPhoto':
    """
    This function is a handler for all incoming messages. It sends a random image of a
    cat with a caption that depends on whether the user is playing a game or not. If the
    user is playing a game, the caption says that the message is not a number. If the user
    is not playing a game, the caption says that the message is not a command.

    Parameters:
    message (Message): The message sent by the user.

    Returns:
    aiogram.methods.send_photo.SendPhoto: A method to send a photo with a caption.

    Raises:
    KeyError: If the user is not registered.
    """
    cur_username = message.from_user.username
    try:
        if users[cur_username]['game']:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_digit'])
        else:
            await message.answer_photo(photo=cats_photos(), caption=texts['text_not_command'])
    except KeyError:
        await message.answer_photo(photo=cats_photos(), caption=texts['registration_requirement_text'])
