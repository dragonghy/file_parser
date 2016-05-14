import cStringIO
import logging


class DataParser(object):
    def __init__(self, path, format):
        self.path = path
        self.format = format

    def _parse_line(self, line):
        buffer = cStringIO.StringIO(line)
        columns = []
        for row_format in self.format.row_formats:
            next_column = buffer.read(row_format.width)
            if len(next_column) != row_format.width:
                raise Exception('Not enough charactors')
            columns.append(row_format.value_of(next_column))
        return columns

    def gen_data(self, chunk_size=100):
        with open(self.path, 'rb') as datafile:
            buffer = []
            for line in datafile:
                # avoid parsing empty line in the end
                if not line:
                    break

                try:
                    buffer.append(self._parse_line(line))
                    if len(buffer) >= chunk_size:
                        yield buffer
                        buffer = []
                except:
                    logging.exception("Invalid line: %s" % line)

            if buffer:
                yield buffer
