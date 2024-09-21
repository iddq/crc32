import crc32
import unittest

from .data import calc4

class Rewind(unittest.TestCase):
    def test_rewind(self):
        c = crc32.CRC32(0xedb88320)
        crc32_reverse = crc32.CRC32Reverse(c)

        for r in calc4:
            self.assertEqual(list(crc32_reverse.find_reverse(*r[:2])), [r[2:]])
