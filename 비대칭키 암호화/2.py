import os
import random
import time
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def generate_key():
    string = bytes(str(os.urandom(32)) + str(random.random()) +
                   str(int(time.time())), 'utf-8')
    key = hashlib.sha256(string).digest()
    key = ''.join('{:02x}'.format(y) for y in key)
    return key


# 생성된 난수의 크기가 p보다 작은지 확인
while True:
    key = generate_key()
    if int(key, 16) < p:
        break

print('개인키(16진수) = 0x' + key)
print('개인키(10진수) =', int(key, 16))

# Double-And-Add
bits = bin(int(key, 16))
bits = bits[2:len(bits)]  # 0b 제거

K = G
bits = bits[1:len(bits)]
for bit in bits:
    if int(bit):  # 1
        K = K*2 + G
    else:  # 0
        K = K*2

print('공개키(16진수) = 0x' + K)
print('공개키(10진수)', int(K, 16))
