from hashlib import sha256
import bitmap


class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.n = 0
        self.bf = bitmap.BitMap(self.m)

    def getPositions(self, item):
        position = []
        for i in range(1, self.k+1):
            position.append(
                int(sha256(item.encode() + str(i).encode()).hexdigest(), 16) % self.m)
        return position

    def add(self, item):
        self.n += 1
        position = self.getPositions(item)
        for i in range(self.k):
            self.bf.set(position[i])

    def contains(self, item):
        position = self.getPositions(item)
        for i in range(self.k):
            if not self.bf[position[i]]:
                return False
        return True

    def reset(self):
        self.n = 0
        self.bf = bitmap.BitMap(self.m)

    def __repr__(self):
        return f"M = {self.m}, F = {self.k}\nBitMap = {self.bf}\n항목의 수 = {self.n}, 1인 비트수 = {self.bf.count()}"


if __name__ == "__main__":
    bf = BloomFilter(53, 3)
    for ch in "AEIOU":
        bf.add(ch)
    print(bf)
    for ch in "ABCDEFGHIJ":
        print(ch, bf.contains(ch))
