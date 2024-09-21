class CRC32:
    def __init__(self, poly: int):
        def table_value(i: int) -> int:
            for _ in range(8):
                i = (i >> 1) ^ (poly & -(i & 1))
            return i

        self.table = tuple(map(table_value, range(256)))

    def calc(self, data: bytes, accum = 0):
        accum = ~accum
        for b in data:
            accum = self.table[(accum ^ b) & 0xFF] ^ ((accum >> 8) & 0x00FFFFFF)
        accum = ~accum
        return accum & 0xFFFFFFFF

class CRC32Reverse(CRC32):
    def __init__(self, poly: int):
        super().__init__(poly)

        self.table_reverse = tuple(
            tuple(j
                  for j in range(256)
                  if self.table[j] >> 24 == i)
            for i in range(256)
        )

    def rewind(self, data: bytes, accum: int) -> set[int]:
        if not data:
            return { accum }
        stack = [(len(data), ~accum)]
        solutions = set()
        while stack:
            node = stack.pop()
            prev_offset = node[0] - 1
            for i in self.table_reverse[(node[1] >> 24) & 0xFF]:
                prevCRC = (((node[1] ^ self.table[i]) << 8) |
                        (i ^ data[prev_offset])) & 0xFFFFFFFF
                if prev_offset:
                    stack.append((prev_offset, prevCRC))
                else:
                    solutions.add((~prevCRC) & 0xFFFFFFFF)
        return solutions

    def find_reverse(self, desired: int, accum = 0) -> set[bytes]:
        solutions = set()
        accum = ~accum
        stack = [(~desired, b'')]
        while stack:
            v, s = stack.pop()
            for j in self.table_reverse[(v >> 24) & 0xFF]:
                next_str = s + bytes([j])
                if len(next_str) == 4:
                    a = accum
                    data = bytearray()
                    for i in range(3, -1, -1):
                        data.append((a ^ next_str[i]) & 0xFF)
                        a >>= 8
                        a ^= self.table[next_str[i]]
                    solutions.add(bytes(data))
                else:
                    stack.append(((v ^ self.table[j]) << 8, next_str))
        return solutions


class Matrix:
    def __init__(self, matrix):
        # column vectors
        self.matrix = matrix

    @staticmethod
    def identity() -> 'Matrix':
        return Matrix(tuple(1 << i for i in range(32)))

    @staticmethod
    def zero_operator(poly: int) -> 'Matrix':
        m = [poly]
        n = 1
        for _ in range(31):
            m.append(n)
            n <<= 1
        return Matrix(tuple(m))

    def multiply_vector(self, v: int, s = 0) -> int:
        for c in self.matrix:
            s ^= c & -(v & 1)
            v >>= 1
            if not v:
                break
        return s

    def mul(self, matrix: 'Matrix') -> 'Matrix':
        return Matrix(tuple(map(self.multiply_vector, matrix.matrix)))

    def sqr(self) -> 'Matrix':
        return self.mul(self)

def combine(c1: int, c2: int, l2: int, n: int, poly: int) -> int:
    # The effect of feeding zero bits into the CRC32 state machine can be
    # represented by matrix multiplication, allowing exponentiation-by-squaring.
    #
    # https://github.com/madler/zlib/blob/v1.2.11/crc32.c#L341-L434
    # https://stackoverflow.com/a/23126768
    #
    # Let C(a) be pure CRC32, and let Z be 32 bits such that
    # C(Z) = 0xffffffff and CRC32(A) = ~C(ZA).
    #
    # Let a be A replaced with zero bits but have the same length as A.
    #
    # CRC32(AB) = ~C(ZAB) = ~(C(ZAb ^ aZb ^ aZB)) = ~(C(ZAb) ^ C(aZb) ^ C(aZB))
    #   = ~C(ZAb) ^ ~C(Zb) ^ ~C(ZB)
    #   = ~(~C(ZAb) ^ C(Zb)) ^ CRC32(B)
    #
    # The first term is ~CRC32(Ab), except the CRC register is negated
    # after A before B.

    m = Matrix.zero_operator(poly)
    m = m.sqr().sqr()

    M = Matrix.identity()
    while l2:
        m = m.sqr()
        if l2 & 1:
            M = m.mul(M)
        l2 >>= 1

    # M is now the matrix that represents appending l2 zero bytes.
    #
    # The effect of matrix multiplication and adding is an affine transform,
    # and homogeneous coordinates allows exponentiation-by-squaring.
    #
    # https://stackoverflow.com/a/59239761

    b = c2
    while True:
        if n & 1:
            c1 = M.multiply_vector(c1, b)

        n >>= 1
        if not n:
            break

        b = M.multiply_vector(b, b)
        M = M.sqr()

    return c1

# Tools

def reverse_bits(x: int) -> int:
    # http://graphics.stanford.edu/~seander/bithacks.html#ReverseParallel
    # http://stackoverflow.com/a/20918545
    x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
    x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
    x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
    x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
    x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
    return x & 0xFFFFFFFF

def reciprocal(poly: int) -> int:
    ''' Return the reciprocal polynomial of a reversed (lsbit-first) polynomial. '''
    return poly << 1 & 0xffffffff | 1
