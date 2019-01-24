from innerjoin.table import Table


class Loader(object):
    @classmethod
    def load(cls, parsed_query):
        return {
            parsed_query['from_table']: Table.load(parsed_query['from_table']),
            parsed_query['join_table']: Table.load(parsed_query['join_table'])
        }
