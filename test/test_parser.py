import pytest
from innerjoin.parser     import Parser
from innerjoin.exceptions import InvalidSyntaxError
from innerjoin.exceptions import InvalidTableError
from innerjoin.exceptions import DuplicateFieldError


def test_sample_query():
    query = """
            SELECT
                nets.version AS version,
                nets.year AS published,
                perf.dataset AS dataset,
                perf.errorrate AS errors
            FROM nets
            INNER JOIN perf
            ON nets.network=perf.network AND nets.version = perf.version
            """

    assert Parser.parse(query) == {
        'from_table': 'nets',
        'join_table': 'perf',
        'fields':     [
            {'table': 'nets', 'name': 'version',   'alias': 'version'},
            {'table': 'nets', 'name': 'year',      'alias': 'published'},
            {'table': 'perf', 'name': 'dataset',   'alias': 'dataset'},
            {'table': 'perf', 'name': 'errorrate', 'alias': 'errors'}
        ],
        'conditions': [
            {'ltable': 'nets', 'lfield': 'network', 'rtable': 'perf', 'rfield': 'network'},
            {'ltable': 'nets', 'lfield': 'version', 'rtable': 'perf', 'rfield': 'version'}
        ]
    }


def test_no_conditions():
    query = "SELECT nets.version AS version FROM nets INNER JOIN perf"
    assert Parser.parse(query) == {
        'from_table': 'nets',
        'join_table': 'perf',
        'fields':     [{'table': 'nets', 'name': 'version',   'alias': 'version'}],
        'conditions': []
    }


def test_uppercase():
    query = "SELECT NETS.VERSION AS VeRsIoN FROM nETs INNER JOIN perf ON nets.network\n \n=PERF.NETWORK"
    assert Parser.parse(query) == {
        'from_table': 'nets',
        'join_table': 'perf',
        'fields':     [{'table': 'nets', 'name': 'version', 'alias': 'VeRsIoN'}],
        'conditions': [{'ltable': 'nets', 'lfield': 'network', 'rtable': 'perf', 'rfield': 'network'}]
    }


def test_invalid_syntax_on_base():
    with pytest.raises(InvalidSyntaxError):
        assert Parser.parse("SELEC nets.version AS version FROM nets INNER JOIN perf")


def test_invalid_syntax_on_fields():
    with pytest.raises(InvalidSyntaxError):
        assert Parser.parse("SELECT nets.versionASversion FROM nets INNER JOIN perf")


def test_invalid_syntax_on_conditions():
    with pytest.raises(InvalidSyntaxError):
        assert Parser.parse("SELECT nets.version AS version FROM nets INNER JOIN perf ON netsversion = perf.version")


def test_invalid_table():
    with pytest.raises(InvalidTableError):
        assert Parser.parse("SELECT nets.version AS version FROM nets INNER JOIN perf ON invalid.version = perf.version")

    with pytest.raises(InvalidTableError):
        assert Parser.parse("SELECT nets.version AS version FROM nets INNER JOIN perf ON nets.version = invalid.version")


def test_duplicate_field():
    with pytest.raises(DuplicateFieldError):
        assert Parser.parse("SELECT nets.version AS version, nets.network AS version FROM nets INNER JOIN perf")
