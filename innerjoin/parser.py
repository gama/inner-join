import re
from innerjoin.exceptions import InvalidSyntaxError
from innerjoin.exceptions import InvalidTableError
from innerjoin.exceptions import DuplicateFieldError


class Parser(object):
    FLAGS           = re.IGNORECASE | re.MULTILINE | re.DOTALL
    ID_REGEX        = r'[A-Z][A-Z0-9]*'
    BASE_REGEX      = re.compile(r'^\s*SELECT\s+(.*)\s+FROM\s+({id})\s+INNER\s+JOIN\s+({id})(?:\s+ON\s+(.*))*$'.format(id=ID_REGEX), FLAGS)
    FIELD_REGEX     = re.compile(r'\s*({id})\.({id})\s+AS\s+({id})\s*'.format(id=ID_REGEX), FLAGS)
    CONDITION_REGEX = re.compile(r'\s*({id})\.({id})\s*=\s*({id})\.({id})'.format(id=ID_REGEX), FLAGS)

    @classmethod
    def parse(cls, query):
        match = cls.BASE_REGEX.match(query)
        if not match:
            raise InvalidSyntaxError("unable to parse base query")

        fields, from_table, join_table, conditions = match.groups()
        from_table = from_table.lower()
        join_table = join_table.lower()
        fields     = cls._parse_fields(fields)
        conditions = cls._parse_conditions(conditions) if conditions else []

        cls._validate_tables_in_conditions(from_table, join_table, conditions)
        cls._validate_field_uniqueness(fields)

        return {
            'from_table': from_table,
            'join_table': join_table,
            'fields':     fields,
            'conditions': conditions
        }

    @classmethod
    def _parse_fields(cls, fields):
        return list(map(cls._parse_field, fields.split(',')))

    @classmethod
    def _parse_field(cls, field):
        match = cls.FIELD_REGEX.match(field)
        if not match:
            raise InvalidSyntaxError('unable to parse select field: ' + field)
        table, field, alias = match.groups()
        return {'table': table.lower(), 'name': field.lower(), 'alias': alias}

    @classmethod
    def _parse_conditions(cls, conditions):
        return list(map(cls._parse_condition, re.split(r'\s+AND\s+', conditions)))

    @classmethod
    def _parse_condition(cls, condition):
        match = cls.CONDITION_REGEX.match(condition)
        if not match:
            raise InvalidSyntaxError('unable to parse select "conditions"')
        ltable, lfield, rtable, rfield = match.groups()
        return {'ltable': ltable.lower(), 'lfield': lfield.lower(),
                'rtable': rtable.lower(), 'rfield': rfield.lower()}

    @classmethod
    def _validate_tables_in_conditions(cls, from_table, join_table, conditions):
        for condition in conditions:
            for cond_table in (condition['ltable'], condition['rtable'],):
                if cond_table not in (from_table, join_table,):
                    raise InvalidTableError('unknown table: ' + cond_table)

    @classmethod
    def _validate_field_uniqueness(cls, fields):
        aliases = set()
        for field in fields:
            if field['alias'] in aliases:
                raise DuplicateFieldError('duplicate field alias: ' + field['alias'])
            aliases.add(field['alias'])
