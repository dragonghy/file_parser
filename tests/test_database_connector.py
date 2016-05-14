from sqlalchemy import inspect
from sqlalchemy.sql.sqltypes import INTEGER, BOOLEAN, VARCHAR
import unittest

from database_connector import SimpleDatabaseConnector
from file_formats import FileFormat


class SimpleDatabaseConnectorTestCase(unittest.TestCase):
    def setUp(self):
        self.connector = SimpleDatabaseConnector('sqlite:///:memory:')

    def test_create_table(self):
        file_format = FileFormat.from_csv('tests/specs/simple_format.csv')
        self.connector.create_table('test_table', file_format)

        inspector = inspect(self.connector.engine)
        columns = inspector.get_columns('test_table')
        self.assertEquals(4, len(columns))

        self.assertDictContainsSubset(
            dict(name='id', primary_key=1),
            columns[0]
        )

        self.assertEquals('name', columns[1]['name'])
        self.assertIsInstance(columns[1]['type'], VARCHAR)
        self.assertEquals('valid', columns[2]['name'])
        self.assertIsInstance(columns[2]['type'], BOOLEAN)
        self.assertEquals('count', columns[3]['name'])
        self.assertIsInstance(columns[3]['type'], INTEGER)

    def test_insert_rows(self):
        file_format = FileFormat.from_csv('tests/specs/simple_format.csv')
        self.connector.create_table('test_table', file_format)

        self.connector.insert_rows([
            ('alice', True, 1),
            ('bob', False, -10),
        ])

        rows = self.connector.engine.execute('SELECT * FROM test_table')
        self.assertEquals(
            [
                (1, u'alice', 1, 1),
                (2, u'bob', 0, -10)
            ],
            list(rows)
        )
