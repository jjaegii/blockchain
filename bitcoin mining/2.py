import time
from hashlib import sha256
max_nonce = 2 ** 32  # 4 billion

msg = input("메시지의 내용? ")
targetbits = input("Target bits? ")


def getTarget(targetbits):
    coefficient = targetbits[2:]
    exponent = int(targetbits[:2], 16)

    backbits = (8*(exponent-3))//4
    frontbits = 58 - backbits

    target = ""
    for i in range(frontbits):
        target += "0"
    target += coefficient
    for i in range(backbits):
        target += "0"

    return target


def POW(msg, target):
    target = int(target, 16)
    extra_nonce = round(time.time())

    for nonce in range(max_nonce):
        hash_result = sha256(
            (msg + str(extra_nonce) + str(nonce)).encode()).hexdigest()
        if int(hash_result, 16) < target:
            return (extra_nonce, nonce, hash_result)
            break
    return None


target = getTarget(targetbits)

start = time.time()
while True:
    result = POW(msg, target)
    if result != None:
        print(f"Target: 0x{target}")
        print(f"메시지: {msg}, Extra nonce = {result[0]}, nonce = {result[1]}")
        print(f"실행 시간: {time.time() - start}초")
        print(f"Hash result: 0x{result[2]}")
        break
