import pytest
from innerjoin.joiner     import Joiner
from innerjoin.table      import Table
from innerjoin.exceptions import InvalidFieldError


def test_sample_query(input_tables):
    query = {
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

    joined_table = Joiner.join(input_tables, query)

    assert joined_table.names == ['version', 'published', 'dataset', 'errors']
    assert joined_table.data  == [
        ['19', '2014', 'ImageNet',    '7.32'],
        ['19', '2014', 'Caltech-256', '14.9'],
        ['v1', '2014', 'ImageNet',    '6.67'],
    ]


def test_no_conditions(input_tables):
    query = {
        'from_table': 'nets',
        'join_table': 'perf',
        'fields':     [
            {'table': 'nets', 'name': 'version',   'alias': 'version'},
            {'table': 'nets', 'name': 'year',      'alias': 'published'},
            {'table': 'perf', 'name': 'dataset',   'alias': 'dataset'},
            {'table': 'perf', 'name': 'errorrate', 'alias': 'errors'}
        ],
        'conditions': []
    }

    joined_table = Joiner.join(input_tables, query)

    assert joined_table.names == ['version', 'published', 'dataset', 'errors']
    assert joined_table.data  == [
        ['19',           '2014', 'ImageNet',    '7.32'],
        ['19',           '2014', 'Caltech-256', '14.9'],
        ['19',           '2014', 'ImageNet',    '6.67'],
        ['19',           '2014', 'ImageNet',    '16.4'],
        ['16-4x pruned', '2017', 'ImageNet',    '7.32'],
        ['16-4x pruned', '2017', 'Caltech-256', '14.9'],
        ['16-4x pruned', '2017', 'ImageNet',    '6.67'],
        ['16-4x pruned', '2017', 'ImageNet',    '16.4'],
        ['v1',           '2014', 'ImageNet',    '7.32'],
        ['v1',           '2014', 'Caltech-256', '14.9'],
        ['v1',           '2014', 'ImageNet',    '6.67'],
        ['v1',           '2014', 'ImageNet',    '16.4']
    ]


def test_no_rows_selected(input_tables):
    query = {
        'from_table': 'nets',
        'join_table': 'perf',
        'fields':     [{'table': 'nets', 'name': 'version',   'alias': 'version'}],
        'conditions': [{'ltable': 'nets', 'lfield': 'network', 'rtable': 'perf', 'rfield': 'version'}]
    }

    joined_table = Joiner.join(input_tables, query)

    assert joined_table.names == ['version']
    assert joined_table.data  == []


def test_invalid_field(input_tables):
    with pytest.raises(InvalidFieldError):
        query = {
            'from_table': 'nets',
            'join_table': 'perf',
            'fields':     [{'table': 'nets', 'name': 'invalid', 'alias': 'version'}],
            'conditions': [{'ltable': 'nets', 'lfield': 'network', 'rtable': 'perf', 'rfield': 'version'}]
        }
        Joiner.join(input_tables, query)

    with pytest.raises(InvalidFieldError):
        query = {
            'from_table': 'nets',
            'join_table': 'perf',
            'fields':     [{'table': 'nets', 'name': 'version', 'alias': 'version'}],
            'conditions': [{'ltable': 'nets', 'lfield': 'network', 'rtable': 'perf', 'rfield': 'invalid'}]
        }
        Joiner.join(input_tables, query)


@pytest.fixture(scope='module')
def input_tables():
    return {
        'nets': Table(
            names = ['network', 'version', 'year'],
            data  = [
                ['VGG',       '19',           '2014'],
                ['VGG',       '16-4x pruned', '2017'],
                ['Inception', 'v1',           '2014']
            ]
        ),
        'perf': Table(
            names = ['network', 'version', 'dataset', 'errorrate'],
            data  = [
                ['VGG',         '19', 'ImageNet',    '7.32'],
                ['VGG',         '19', 'Caltech-256', '14.9'],
                ['Inception',   'v1', 'ImageNet',    '6.67'],
                ['SuperVision', '?',  'ImageNet',    '16.4']
            ]
        )
    }
