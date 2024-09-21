import crc32
import unittest

from .test_data import flip, reciprocal, tables, edb88320_reverse, calc, calc4

class ParserFunctions(unittest.TestCase):

    def setUp(self):
        self.crc32 = crc32.CRC32(0xedb88320)
        self.crc32_reverse = crc32.CRC32Reverse(self.crc32)

    # Tests
    def test_flip(self):
        for k, v in flip.items():
            self.assertEqual(crc32.reverse_bits(k), v)
            self.assertEqual(crc32.reverse_bits(crc32.reverse_bits(k)), k)
            self.assertEqual(
                crc32.reverse_bits(crc32.reverse_bits(v)), v)

    def test_reciprocal(self):
        for k, v in reciprocal.items():
            self.assertEqual(crc32.reverse_bits(crc32.reciprocal(k)), v)
            self.assertEqual(crc32.reverse_bits(crc32.reciprocal(v)), k)

    def test_table(self):
        for k, v in tables.items():
            self.assertEqual(crc32.CRC32(k).table, v)
        # reverse table for 0xedb88320 only
        self.assertEqual(
            tuple(map(lambda x: x[0], self.crc32_reverse.table_reverse)), edb88320_reverse)

    def test_undo_one_solution(self):
        for c in calc:
            bytes = tuple(map(ord, c[2]))
            self.assertEqual(list(self.crc32_reverse.rewind(bytes, c[0])), [c[1]])

    def test_undo_multiple_solutions(self):
        pass

    def test_calc(self):
        for c in calc:
            bytes = tuple(map(ord, c[2]))
            self.assertEqual(self.crc32.calc(bytes, c[1]), c[0])
        for c in calc4:
            self.assertEqual(self.crc32.calc(c[2:], c[1]), c[0])

    def test_reverse(self):
        for r in calc4:
            self.assertEqual(list(self.crc32_reverse.find_reverse(*r[:2])), [r[2:]])
