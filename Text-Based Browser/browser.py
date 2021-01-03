import os
import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore, Style
from _collections import deque


args = sys.argv
folder = args[1]

if not os.path.exists(folder):
    os.mkdir(folder)

history = deque()


def url_format(user):
    if 'https://' in user:
        return user
    else:
        return 'https://' + user


def file_format(user):
    return user[:user.rindex('.')] if '.' in user else user


def open_site(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = ""
    for tag in soup.find_all(["a", "p", "head", "ul", "ol", "li"]):
        if tag.name == "a":
            text += Fore.BLUE + tag.text.strip() + "\n"
        else:
            text += Style.RESET_ALL + tag.text.strip() + "\n"
    return text


while True:
    user = input()
    if user == 'exit':
        break

    tab = os.path.join(folder, file_format(user))

    if os.path.exists(tab):
        with open(tab) as file:
            print(file.read())

    elif user == 'back':
        history.pop()
        if history:
            prev = os.path.join(folder, history.pop())
            with open(prev) as file:
                print(file.read())
        else:
            continue

    elif '.' in user:
        with open(os.path.join(folder, file_format(user)), 'w') as file:
            file.writelines(open_site(url_format(user)))
            print(open_site(url_format(user)))
        history.append(file_format(user))

    else:
        print('error')
