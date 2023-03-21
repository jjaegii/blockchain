import os
import random
import time
import hashlib
import math

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
e1 = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
      0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
a = 0
b = 7
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def generate_private_key():
    while True:
        random_str = os.urandom(
            256 // 8) + str(random.random()).encode() + str(time.time()).encode()
        random_num = hashlib.sha256(random_str).digest()
        private_key = int.from_bytes(random_num, 'big')
        if private_key < p:
            break
    return private_key


def euclidian(b, n):
    r1 = n
    r2 = b if b > 0 else b+n
    t1 = 0
    t2 = 1
    while r2 > 0:
        q = r1 // r2
        r = r1 - q * r2
        r1 = r2
        r2 = r
        t = t1 - q * t2
        t1 = t2
        t2 = t
    if r1 == 1:
        return t1 if t1 > 0 else t1 + n
    else:
        return None


def add(point1: tuple, point2: tuple):
    if point1 == point2:
        w = (3 * point1[0] ** 2 + a) * euclidian((2 * point1[1]), p) % p
    else:
        w = (point2[1] - point1[1]) * euclidian(point2[0] - point1[0], p) % p
    if w < 0:
        w += p
    x3 = (w ** 2 - point1[0] - point2[0]) % p
    y3 = (w * (point1[0] - x3) - point1[1]) % p
    if x3 < 0:
        x3 += p
    if y3 < 0:
        y3 += p
    point3 = (x3, y3)
    return point3


def double_and_add(x, G: list):
    binary = bin(x)
    K = G
    for i in range(3, len(binary)):
        if binary[i] == '1':
            K = add(add(K, K), G)
        else:
            K = add(K, K)

    return tuple(K)


def generate_public_key(x):
    return double_and_add(x, e1)


def sign(M, d):
    while True:
        r = random.randint(1, q-1)
        P = double_and_add(r, e1)
        if P[0] == 0:
            continue
        H = int.from_bytes(hashlib.sha256(
            M.encode()).digest(), byteorder='big') % q
        S1 = P[0] % q
        S2 = (H + d * S1) * euclidian(r, q) % q
        return S1, S2


def verify(M, S1, S2, e2):
    H = int.from_bytes(hashlib.sha256(
        M.encode()).digest(), byteorder='big') % q
    print(H)
    A = H * euclidian(S2, q) % q
    B = S1 * euclidian(S2, q) % q
    T = add(double_and_add(A, e1), double_and_add(B, e2))
    return T[0] % q == S1 % q


if __name__ == "__main__":
    d = generate_private_key()  # 2주차 과제에서 작성한 함수
    e2 = generate_public_key(d)  # 2주차 과제에서 작성한 함수

    M = input("메시지? ")
    S1, S2 = sign(M, d)
    print("1. Sign:")
    print("\tS1 =", hex(S1))
    print("\tS2 =", hex(S2))

    print("2. 정확한 서명을 입력할 경우:")
    if verify(M, S1, S2, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")

    print("3. 잘못된 서명을 입력할 경우:")
    if verify(M, S1-1, S2-1, e2) == True:
        print("검증 성공")
    else:
        print("검증 실패")
