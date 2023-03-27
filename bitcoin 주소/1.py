from Crypto.Hash import RIPEMD160
import base58check
import hashlib

k = int(input('개인키입력? '), 16)
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
a = 0
b = 7
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


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


def double_and_add(x, G: tuple):
    binary = bin(x)
    K = G
    for i in range(3, len(binary)):
        if binary[i] == '1':
            K = add(add(K, K), G)
        else:
            K = add(K, K)

    return tuple(K)


# 공개키
x, y = double_and_add(k, G)

# 짝수면 02, 홀수면 03 앞에 붙음
if y % 2 == 0:
    x = '02' + hex(x)[2:]
else:
    x = '03' + hex(x)[2:]

x = hashlib.sha256(bytes.fromhex(x)).digest()
h = RIPEMD160.new()
h.update(x)
h = '00' + h.hexdigest()

print('공개키 hash =', h)

h_sha256 = hashlib.sha256(bytes.fromhex(h)).digest()
h_sha256_sha256 = hashlib.sha256(h_sha256).digest()
checksum = h_sha256_sha256.hex()[:8]
bitcoin_address = base58check.b58encode(bytes.fromhex(h + checksum))

print('비트코인 주소 =', bitcoin_address.decode('utf-8'))
