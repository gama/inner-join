from innerjoin.table      import Table
from innerjoin.exceptions import InvalidFieldError


class Joiner(object):
    @classmethod
    def join(cls, input_tables, query):
        cls._add_indexes_to_fields(query['fields'], input_tables)
        cls._add_indexes_to_conditions(query['conditions'], input_tables)
        return cls._slowjoin(input_tables, query)
        # return cls._fastjoin(input_tables, query)

    @classmethod
    def _slowjoin(cls, input_tables, query):
        return cls._cartesian_product(input_tables, query)

    @classmethod
    def _fastjoin(cls, input_tables, query):
        cls._add_indexes_to_fields(query['fields'], input_tables)
        cls._add_indexes_to_conditions(query['conditions'], input_tables)

        if not query['conditions']:
            return cls._cartesian_product(input_tables, query)
        # TODO: sort by conditions and then implement a mergejoin

    @classmethod
    def _cartesian_product(cls, input_tables, query):
        field_aliases = [field['alias'] for field in query['fields']]
        joined_table  = Table(names=field_aliases)

        from_table = input_tables[query['from_table']]
        join_table = input_tables[query['join_table']]
        for from_row in from_table.data:
            for join_row in join_table.data:
                row_data = {query['from_table']: from_row, query['join_table']: join_row}
                if cls._row_meets_conditions(row_data, query['conditions']):
                    cls._add_fields(joined_table, row_data, query['fields'])

        return joined_table

    @classmethod
    def _add_indexes_to_fields(cls, fields, input_tables):
        for field in fields:
            try:
                field['index'] = input_tables[field['table']].names.index(field['name'])
            except ValueError:
                raise InvalidFieldError('unable to find select field {} in table {}'.format(
                    field['name'], field['table']))

    @classmethod
    def _add_indexes_to_conditions(cls, conditions, input_tables):
        for condition in conditions:
            for idx, table, field in (('lindex', 'ltable', 'lfield'), ('rindex', 'rtable', 'rfield'),):
                try:
                    condition[idx] = input_tables[condition[table]].names.index(condition[field])
                    condition[idx] = input_tables[condition[table]].names.index(condition[field])
                except ValueError:
                    raise InvalidFieldError('unable to find condition field {} in table {}'.format(
                        condition[field], condition[table]))

    @classmethod
    def _row_meets_conditions(cls, row_data, conditions):
        return all([cls._row_meets_condition(row_data, condition) for condition in conditions])

    @classmethod
    def _row_meets_condition(cls, row_data, condition):
        return row_data[condition['ltable']][condition['lindex']] == \
               row_data[condition['rtable']][condition['rindex']]

    @classmethod
    def _add_fields(cls, joined_table, row_data, fields):
        joined_row = [
            row_data[field['table']][field['index']]
            for field in fields
        ]
        joined_table.data.append(joined_row)
