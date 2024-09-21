import crc32
import unittest

cases = (
    (0x00000000, 0x00000000),
    (0x80000000, 0x00000001),
    (0x04c11db7, 0xedb88320),
    (0x1edc6f41, 0x82f63b78),
    (0x741b8cd7, 0xeb31d82e),
    (0x814141ab, 0xd5828281),
)

class Reverse(unittest.TestCase):
    def test_reverse(self):
        for k, v in cases:
            self.assertEqual(crc32.reverse_bits(k), v)
            self.assertEqual(crc32.reverse_bits(crc32.reverse_bits(k)), k)
            self.assertEqual(crc32.reverse_bits(crc32.reverse_bits(v)), v)
