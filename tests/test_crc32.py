import crc32
import unittest

calc = (
    # (hash, accum, str),
    (0x00000000, 0x00000000, (0x9d, 0x0a, 0xd9, 0x6d)),
    (0x13371337, 0x00000000, (0x6c, 0x37, 0x8b, 0xf4)),
    (0x00000000, 0x00000000, ''),
    (0xcbf43926, 0x00000000, '123456789'),
    (0x352441c2, 0x00000000, 'abc'),
    (0x00000000, 0x00000000, '4kESJM'),
    (0x00000000, 0x00000000, 'CN3h0f'),
    (0x00000000, 0x00000000, 'Fk1HCP'),
    (0x00000000, 0x00000000, 'GkpyXI'),
    (0x00000000, 0x00000000, 'IdoIdG'),
    (0x00000000, 0x00000000, 'R24vZl'),
    (0x00000000, 0x00000000, 'S2uGAu'),
    (0x00000000, 0x00000000, 'VZZZ_K'),
    (0x00000000, 0x00000000, 'WFT7EF'),
    (0x00000000, 0x00000000, 'XUEjcE'),
    (0x00000000, 0x00000000, '_LBTIn'),
    (0x00000000, 0x00000000, 'vUicdN'),
    (0x00000000, 0x00000000, 'yZ7bCY'),
    (0x13371337, 0x00000000, '1QCCco'),
    (0x13371337, 0x00000000, 'Am2F3o'),
    (0x13371337, 0x00000000, 'BQviqk'),
    (0x13371337, 0x00000000, 'CQ7Xjr'),
    (0x13371337, 0x00000000, 'G9YtoU'),
    (0x13371337, 0x00000000, 'KGnggN'),
    (0x13371337, 0x00000000, 'MBg4Wh'),
    (0x13371337, 0x00000000, 'T4vI1J'),
    (0x13371337, 0x00000000, 'XJAZ9Q'),
    (0x13371337, 0x00000000, 'c2wLU3'),
    (0x13371337, 0x00000000, 'g6jMTP'),
    (0x13371337, 0x00000000, 'h94LsG'),
    (0x13371337, 0x00000000, 'jTS3FF'),
    (0x13371337, 0x00000000, 'soosMl'),
    (0x13371337, 0x00000000, 'tvhMgG'),
)

def to_bytes(data):
    if isinstance(data, str):
        return bytes(data, encoding='utf8')
    return bytes(data)

class Calc(unittest.TestCase):
    def setUp(self):
        self.crc32 = crc32.CRC32(0xedb88320)
        self.crc32_reverse = crc32.CRC32Reverse(self.crc32)

    def test(self):
        for c in calc:
            b = to_bytes(c[2])

            checksum = self.crc32.calc(b, c[1])
            self.assertEqual(checksum, c[0])

            self.assertSetEqual(self.crc32_reverse.rewind(b, c[0]), { c[1] })

            if len(b) == 4:
                self.assertSetEqual(self.crc32_reverse.find_reverse(*c[:2]), { c[2] })

            self.assertEqual(crc32.combine(c[1], checksum, len(b), 1009, 0xedb88320), self.crc32.calc(b * 1009, c[1]))
