import os
import random
import re

import requests

length = 5


def check_usernames(filters_set, token_user, chatid, length):
    if os.path.exists(f'checked_usernames_{length}.txt'):
        with open(f'checked_usernames_{length}.txt', 'r') as f:
            checked_usernames_file = f.read().split('\n')
    else:
        with open(f'checked_usernames_{length}.txt', 'w'):
            pass
        with open(f'checked_usernames_{length}_free.txt', 'w'):
            pass
    checked_usernames = []
    checked_usernames_free = []
    if not filters_set:
        symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v',
                   'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_']
        weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 200]
    elif filters_set == set('1'):
        symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v',
                   'w', 'x', 'y', 'z', '_']
        weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 150]
    elif filters_set == set('2'):
        symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v',
                   'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    else:
        symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v',
                   'w', 'x', 'y', 'z']
    while True:
        try:
            username = ''.join(random.choices(symbols, k=length, weights=weights))
            if (username not in checked_usernames_file and username not in checked_usernames
                and not username[0].isdigit() and not username[0] == '_' and not username[-1] == '_') and not re.search(
                r"_{2,}", username):
                checked_usernames.append(username)
                r = requests.get(f'https://fragment.com/username/{username}', timeout=10).text
                if 'Not for sale' in r:
                    send_telegram_message(f"✅Username: {username}", token_user, chatid)
                    checked_usernames_free.append(username)
                    print(f"✅Username: {username}")
                else:
                    print(f"❌Username: {username}")
        except KeyboardInterrupt:
            with open(f'checked_usernames_{length}.txt', 'a') as f:
                f.write("\n".join(checked_usernames))
            with open(f'checked_usernames_{length}_free.txt', 'a') as f:
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

    print()
    print('Фильтры:')
    print('1. Без цифр (0-9)    2. Без нижнего подчеркивания (_)')
    print()
    filters_list = ['1', '2']
    while True:
        filters = set(input('Укажите фильтры (через пробел) или оставьте поле пустым: ').split())
        if len(filters) <= 2 and all(i in filters_list for i in filters):
            break
        print('Неверно введены фильтры!')
    while True:
        length = input('Введите длину юзернейма: ')
        if length.isdigit() and int(length) > 3:
            length = int(length)
            break
        print('Длина введена неверно!')

    check_usernames(filters, token, chat_id, length)
