# -*- coding: utf-8 -*-
import unittest

from file_formats import FileFormat
from file_formats import FilenamePrefixFormatSelector


class FileFormatTestCase(unittest.TestCase):
    def test_simple_format(self):
        file_format = FileFormat.from_csv('tests/specs/simple_format.csv')

        self.assertEquals(3, len(file_format.row_formats))

        self.assertEquals('name', file_format.row_formats[0].name)
        self.assertEquals(10, file_format.row_formats[0].width)
        self.assertEquals('TEXT', file_format.row_formats[0].datatype)

        self.assertEquals('valid', file_format.row_formats[1].name)
        self.assertEquals(1, file_format.row_formats[1].width)
        self.assertEquals('BOOLEAN', file_format.row_formats[1].datatype)

        self.assertEquals('count', file_format.row_formats[2].name)
        self.assertEquals(3, file_format.row_formats[2].width)
        self.assertEquals('INTEGER', file_format.row_formats[2].datatype)

    def test_unicode_format(self):
        file_format = FileFormat.from_csv('tests/specs/unicode_format.csv')

        self.assertEquals(1, len(file_format.row_formats))

        self.assertEquals(u'名字'.encode('utf-8'), file_format.row_formats[0].name)
        self.assertEquals(10, file_format.row_formats[0].width)
        self.assertEquals('TEXT', file_format.row_formats[0].datatype)


class PrefixFormatSelectorTestCase(unittest.TestCase):
    def test_select_format(self):
        selector = FilenamePrefixFormatSelector.from_directory('tests/specs/')
        self.assertIn('simple_format', selector.format_dict)
        self.assertIn('unicode_format', selector.format_dict)
        self.assertIsNotNone(selector.get_format('tests/data/simple_format_2015-06-28.txt'))
        self.assertIsNotNone(selector.get_format('tests/data/unicode_format_2011-06-28.txt'))
        self.assertIsNone(selector.get_format('tests/data/not_exist_format_2011-06-28.txt'))

        # no underscore in date string
        self.assertIsNone(selector.get_format('tests/data/simple_format_2011_06_28.txt'))
