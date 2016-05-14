# -*- coding: utf-8 -*-
import unittest

from data_parser import DataParser
from file_formats import FileFormat


class DataParserTestCase(unittest.TestCase):
    def test_parse_data(self):
        file_format = FileFormat.from_csv('tests/specs/simple_format.csv')
        parser = DataParser('tests/data/simple_format_2015-06-28.txt', file_format)

        self.assertEquals(
            [[['Foonyor', 1, 1], ['Barzane', 0, -12], ['Quuxitude', 1, 103]]],
            list(parser.gen_data())
        )

        self.assertEquals(
            [[['Foonyor', 1, 1], ['Barzane', 0, -12]], [['Quuxitude', 1, 103]]],
            list(parser.gen_data(chunk_size=2))
        )

        self.assertEquals(
            [[['Foonyor', 1, 1]], [['Barzane', 0, -12]], [['Quuxitude', 1, 103]]],
            list(parser.gen_data(chunk_size=1))
        )

    def test_parse_unicode_data(self):
        file_format = FileFormat.from_csv('tests/specs/simple_format.csv')
        parser = DataParser('tests/data/simple_format_2015-06-28-unicode.txt', file_format)

        self.assertEquals(
            [[['Foonyor', 1, 1], [u'Barzàne'.encode('utf-8'), 0, -12]]],
            list(parser.gen_data())
        )
