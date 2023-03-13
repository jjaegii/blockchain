# Vigenere 암호
sentence = input("평문 입력: ").replace(" ", "").upper()
vigenere = input("Vigenere 암호? ").upper()

encrypted = ""
# 암호화
for i in range(len(sentence)):
    encrypted_chr = ord(sentence[i]) + \
        ord(vigenere[i % (len(vigenere))]) - 65
    if encrypted_chr > 90:
        encrypted_chr -= 26
    encrypted += chr(encrypted_chr)

print("암호문:", encrypted)

decrypted = ""
# 복호화
for i in range(len(encrypted)):
    decrypted_chr = ord(encrypted[i]) - (ord(vigenere[i % len(vigenere)]) - 65)
    if decrypted_chr < 65:
        decrypted_chr += 26
    decrypted += chr(decrypted_chr)

print("평문:", decrypted)

# 자동 키 암호
autokey = int(input("자동 키 암호? "))
encrypted = ""
# 암호화
encrypted_chr = ord(sentence[0]) + autokey
if encrypted_chr > 90:
    encrypted_chr -= 26
encrypted += chr(encrypted_chr)
for i in range(1, len(sentence)):
    encrypted_chr = ord(sentence[i]) + ord(sentence[i-1]) - 65
    if encrypted_chr > 90:
        encrypted_chr -= 26
    encrypted += chr(encrypted_chr)

print("암호문:", encrypted)

decrypted = ""
# 복호화
decrypted_chr = ord(encrypted[0]) - autokey
if decrypted_chr < 65:
    decrypted_chr += 26
decrypted += chr(decrypted_chr)
for i in range(1, len(encrypted)):
    decrypted_chr = ord(encrypted[i]) - (ord(decrypted[i-1]) - 65)
    if decrypted_chr < 65:
        decrypted_chr += 26
    decrypted += chr(decrypted_chr)

print("평문:", decrypted)
