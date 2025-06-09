import os
import random
import re

import requests

length = 5


def check_usernames(chatid, token_user, txt_file):
    if os.path.exists(f'checked_usernames_{txt_file.split(".")[0]}.txt'):
        with open(f'checked_usernames_{txt_file.split(".")[0]}.txt', 'r') as f:
            checked_usernames_file = f.read().split('\n')
    else:
        with open(f'checked_usernames_{txt_file.split(".")[0]}.txt', 'w'):
            pass
        with open(f'checked_usernames_{txt_file.split(".")[0]}_free.txt', 'w'):
            pass
        with open(f'checked_usernames_{txt_file.split(".")[0]}.txt', 'r') as f:
            checked_usernames_file = f.read().split('\n')
    with open(f'{txt_file}', 'r') as f:
        txt_usernames = f.read().split('\n')
    checked_usernames = []
    checked_usernames_free = []
    for i in txt_usernames:
        try:
            username = i
            if (username not in checked_usernames_file and username not in checked_usernames
                and not username[0].isdigit() and username[0] != '_' and username[-1] != '_' and 32 >= len(
                        username) > 3) and not re.search(
                r"_{2,}", username):
                checked_usernames.append(username)
                r = requests.get(f'https://fragment.com/username/{username}', timeout=10).text
                if 'Not for sale' in r:
                    send_telegram_message(f"✅Username: {username}", token_user, chatid)
                    checked_usernames_free.append(username)
                    print(f"✅Username: {username}")
                else:
                    print(f"❌Username: {username}")
        except:
            with open(f'checked_usernames_{txt_file.split(".")[0]}.txt', 'a') as f:
                f.write("\n".join(checked_usernames))
            with open(f'checked_usernames_{txt_file.split(".")[0]}_free.txt', 'a') as f:
                f.write("\n".join(checked_usernames_free))


def send_telegram_message(message, token_user, chatid):
    url = f"https://api.telegram.org/bot{token_user}/sendMessage"
    payload = {
        'chat_id': chatid,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    return requests.post(url, data=payload, timeout=10)


if __name__ == '__main__':
    print('Генератор юзернеймов Telegram.')
    token = input('Укажите токен вашего телеграм бота (бот будет отправлять вам незанятые юзернеймы): ')
    while not requests.get(f'https://api.telegram.org/bot{token}/getMe').json()['ok']:
        print('Токен введён неверно!')
        token = input('Укажите токен вашего телеграм бота (бот будет отправлять вам незанятые юзернеймы): ')

    chat_id = input(
        'Укажите ваш телеграм id (бот будет присылать по этому id юзернеймы, получить id можно тут @getmyid_bot): ')
    while not requests.get(f'https://api.telegram.org/bot{token}/getChat?chat_id={chat_id}').json()['ok']:
        print('ID введён неверно или вы не написали боту!')
        chat_id = input(
            'Укажите ваш телеграм id (бот будет присылать по этому id юзернеймы, получить id можно тут @getmyid_bot): ')

    while True:
        txt_file = input('Введите название текстового файла (вместе с расширением) для чтения юзернеймов: ')
        if os.path.exists(f'{txt_file}'):
            break
        print('Текстовой файл не найден!')

    check_usernames(chat_id, token, txt_file)
