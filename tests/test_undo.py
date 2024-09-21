import crc32
import unittest

from .data import calc

class Undo(unittest.TestCase):
    def setUp(self):
        self.crc32 = crc32.CRC32(0xedb88320)
        self.crc32_reverse = crc32.CRC32Reverse(self.crc32)

    def test_undo_one_solution(self):
        for c in calc:
            bytes = tuple(map(ord, c[2]))
            self.assertEqual(list(self.crc32_reverse.rewind(bytes, c[0])), [c[1]])

    def test_undo_multiple_solutions(self):
        pass
