import csv
from distutils.util import strtobool
import glob

from sqlalchemy import Column, String, Integer, Boolean

from utils import get_filename_from_path


class RowFormat(object):
    SQL_TYPE_MAPPING = {
        'TEXT': String,
        'INTEGER': Integer,
        'BOOLEAN': Boolean,
    }

    VALUE_CONVERTOR_MAPPING = {
        'TEXT': lambda value: value.strip(),
        'INTEGER': int,
        'BOOLEAN': strtobool,
    }

    def __init__(self, name, width, datatype):
        self.name = name
        self.width = int(width)
        self.datatype = datatype
        self.value_converter = self.VALUE_CONVERTOR_MAPPING.get(self.datatype)

    def to_sql_column(self):
        return Column(
            self.name,
            self.SQL_TYPE_MAPPING.get(self.datatype)
        )

    def value_of(self, value):
        return self.value_converter(value)


class FileFormat(object):
    def __init__(self, path, row_formats):
        self.path = path
        self.row_formats = row_formats

    @classmethod
    def from_csv(cls, csv_filename):
        with open(csv_filename, 'rb') as csvfile:
            rows = list(csv.reader(csvfile))
            # take out the headers
            rows = rows[1:]
            return FileFormat(csv_filename, [RowFormat(*row) for row in rows])
            # TODO validation


class FormatSelector(object):
    def __init__(self, formats):
        self.formats = formats

    def get_format(self, path):
        """Get format from filename.

        To be implemented by child classes"""
        pass

    @classmethod
    def from_directory(cls, directory):
        format_filenames = glob.glob('%s/*.csv' % directory)
        return cls([FileFormat.from_csv(format_filename) for format_filename in format_filenames])


class FilenamePrefixFormatSelector(FormatSelector):
    """Format selector based on filename prefix"""
    def __init__(self, formats):
        super(FilenamePrefixFormatSelector, self).__init__(formats)
        self.format_dict = {
            get_filename_from_path(format.path): format
            for format in formats
        }

    def get_format(self, path):
        filename = get_filename_from_path(path)
        format_name, _ = filename.rsplit('_', 1)
        return self.format_dict.get(format_name)
