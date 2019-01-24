import os
from io import StringIO
from innerjoin.exceptions import MissingTableError


class Table(object):
    def __init__(self, names=None, data=None):
        self.names = names or []
        self.data  = data  or []

    def print(self):
        print(self.serialize(), end='')

    def serialize(self):
        sio = StringIO()
        print('\t'.join(self.names), file=sio)
        for row in self.data:
            print('\t'.join(row), file=sio)
        return sio.getvalue()

    @classmethod
    def load(cls, table_name):
        file_name = table_name + '.tsv'
        if not os.path.exists(file_name):
            raise MissingTableError('unable to find input table file: ' + file_name)
        return cls._load_from_file(file_name)

    @classmethod
    def _load_from_file(cls, file_name):
        with open(file_name) as file:
            return cls(
                names = file.readline().strip().lower().split('\t'),
                data  = [line.strip().split('\t') for line in file]
            )
