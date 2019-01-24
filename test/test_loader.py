import os
import pytest
from innerjoin.loader     import Loader
from innerjoin.exceptions import MissingTableError


def test_load_sample_tables(chdir):
    input_tables = Loader.load({'from_table': 'nets', 'join_table': 'perf'})
    assert sorted(input_tables.keys()) == ['nets', 'perf']
    assert input_tables['nets'].names  == ['network', 'version', 'year']
    assert input_tables['nets'].data   == [
        ['VGG',       '19',           '2014'],
        ['VGG',       '16-4x pruned', '2017'],
        ['Inception', 'v1',           '2014']
    ]
    assert input_tables['perf'].names  == ['network', 'version', 'dataset', 'errorrate']
    assert input_tables['perf'].data   == [
        ['VGG',         '19', 'ImageNet',    '7.32'],
        ['VGG',         '19', 'Caltech-256', '14.9'],
        ['Inception',   'v1', 'ImageNet',    '6.67'],
        ['SuperVision', '?',  'ImageNet',    '16.4']
    ]


def test_missing_table(chdir):
    with pytest.raises(MissingTableError):
        Loader.load({'from_table': 'invalid', 'join_table': 'perf'})

    with pytest.raises(MissingTableError):
        Loader.load({'from_table': 'nets', 'join_table': 'invalid'})


@pytest.fixture(scope='module')
def chdir():
    pwd = os.path.realpath(os.curdir)
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
    os.chdir(data_dir)
    yield
    os.chdir(pwd)
