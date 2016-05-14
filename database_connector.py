from sqlalchemy import create_engine, Column, Integer, MetaData, Table


class SimpleDatabaseConnector(object):
    def __init__(self, url):
        self.engine = create_engine(url)
        self.table = None

    def create_table(self, table_name, file_format):
        self.table = Table(
            table_name,
            MetaData(bind=self.engine),
            Column('id', Integer, primary_key=True),
            *[row_format.to_sql_column() for row_format in file_format.row_formats]
        )
        self.column_names = [rowformat.name for rowformat in file_format.row_formats]
        self.table.create()

    def insert_rows(self, rows):
        translated_rows = [
            dict(zip(self.column_names, row))
            for row in rows
        ]
        self.table.insert().execute(translated_rows)
