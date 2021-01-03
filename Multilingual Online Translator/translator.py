import requests
import sys
from bs4 import BeautifulSoup


languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese',
             8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}


args = sys.argv
lang_1, lang_2, word = args[1], args[2], args[3]

try:
    lang_1 = list(languages.keys())[list(languages.values()).index(lang_1.title())]
except ValueError:
    print(f'Sorry, the program doesn\'t support {lang_1}')
    sys.exit()

if lang_2.title() not in languages.values() and lang_2 != 'all':
    print(f'Sorry, the program doesn\'t support {lang_2}')
    sys.exit()


# ----- without sys.args ------
# def choose_translation():
#     print('Hello, you\'re welcome to the translator. Translator supports: ')
#     for k, v in languages.items():
#         print(str(k) + '.', v)
#
#     lang_1 = int(input('Type the number of your language:\n'))
#     lang_2 = int(input('Type the number of a language you want to translate to'
#                        ' or \'0\' to translate to all languages:\n'))
#     if lang_2 > 0:
#         lang_2 = languages[lang_2]
#     word = input('Type the word you want to translate:\n')
#
#     return lang_1, lang_2, word


def get_connection(lang_1, lang_2, word):
    lang_1 = languages[lang_1]
    user_agent = 'Mozilla/5.0'
    url = f'https://context.reverso.net/translation/{lang_1.lower()}-{lang_2.lower()}/{word}'
    try:
        response = requests.get(url, headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()

    return response


def translation(lang_2, word, response, lines=5):
    soup = BeautifulSoup(response.content, 'html.parser')
    words = soup.find_all('a', {'class': 'dict'})
    sentences = soup.find_all('div', {'class': 'example'})

    word_lst = [word.text.strip() for word in words]
    sentence_lst = [sentence.text.strip().replace(('\n' * 5) + (' ' * 10), '\n') for sentence in sentences]

    if len(word_lst) == 0:
        print(f'Sorry, unable to find {word}')
        sys.exit()

    with open(f'{word}.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{lang_2} Translations:\n')
        for word in word_lst[:lines]:
            f.write(word + '\n')
        f.write('\n')
        f.write(f'{lang_2} Examples:\n')
        for sentence in sentence_lst[:lines]:
            f.write(sentence + '\n' * 2)
        f.write('\n')
        f.seek(0)
        print(f.read())


def main():
    choose = (lang_1, lang_2, word)
    file = open(f'{choose[2]}.txt', 'w')
    file.close()

    if choose[1] != 'all':
        connect = get_connection(*choose)
        translation(choose[1], choose[2], connect)
    else:
        trans = languages.copy()
        del trans[choose[0]]
        for t in trans:
            connect = get_connection(choose[0], languages[t], choose[2])
            translation(languages[t], choose[2], connect, lines=1)


main()
