import crc32
import unittest

from .data import calc, calc4

class Calc(unittest.TestCase):

    def test_calc(self):
        crc = crc32.CRC32(0xedb88320)

        for c in calc:
            bytes = tuple(map(ord, c[2]))
            self.assertEqual(crc.calc(bytes, c[1]), c[0])
        for c in calc4:
            self.assertEqual(crc.calc(c[2:], c[1]), c[0])
