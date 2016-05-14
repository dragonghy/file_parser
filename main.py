import argparse
import glob
import itertools

from data_parser import DataParser
from database_connector import SimpleDatabaseConnector
from file_formats import FilenamePrefixFormatSelector

parser = argparse.ArgumentParser(description='Process data file and store to SQL.')
parser.add_argument('db_url', help='Database url')
parser.add_argument('table_name', help='Database table to create')
parser.add_argument('data_file', help='Data file to dump')

args = parser.parse_args()

# init
format_selector = FilenamePrefixFormatSelector.from_directory('specs/')
format = format_selector.get_format(args.data_file)
data_parser = DataParser(args.data_file, format)
db_connector = SimpleDatabaseConnector(args.db_url)

print 'Creating table ...'
db_connector.create_table(args.table_name, format)  # TODO rollback on failure?

print 'Insertion rows ...'
total_inserted = 0
for rows in data_parser.gen_data():
    db_connector.insert_rows(rows)
    total_inserted += len(rows)
    print '%d rows inserted' % total_inserted

print 'Completed'
