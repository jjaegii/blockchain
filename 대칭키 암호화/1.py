import random
from string import ascii_lowercase

key = list(ascii_lowercase)
value = list(ascii_lowercase)
random.shuffle(value)

E = {}
D = {}
for i in range(len(key)):
    E[key[i]] = value[i]
    D[value[i]] = key[i]

sentence = input('평문 입력: ')
encrypted = ''
for i in range(len(sentence)):
    if sentence[i] == ' ':
        encrypted += ' '
    else:
        encrypted += E[sentence[i]]

print("암호문:", encrypted)

decrypted = ''
for i in range(len(encrypted)):
    if encrypted[i] == ' ':
        decrypted += ' '
    else:
        decrypted += D[encrypted[i]]

print('복호문:', decrypted)
