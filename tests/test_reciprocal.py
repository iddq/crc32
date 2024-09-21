import crc32
import unittest

cases = (
    (0xedb88320, 0x82608edb),
    (0x82f63b78, 0x8f6e37a0),
    (0xeb31d82e, 0xba0dc66b),
    (0xd5828281, 0xc0a0a0d5),
)

class Reciprocal(unittest.TestCase):
    def test_reciprocal(self):
        for k, v in cases:
            self.assertEqual(crc32.reverse_bits(crc32.reciprocal(k)), v)
            self.assertEqual(crc32.reverse_bits(crc32.reciprocal(v)), k)
