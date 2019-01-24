from innerjoin.table import Table


def test_serialize():
    table = Table(
        names = ['network', 'version', 'years'],
        data  = [
            ['VGG',       '19',           '2014'],
            ['VGG',       '16-4x pruned', '2017'],
            ['Inception', 'v1',           '2014']
        ]
    )
    expected = 'network	version	years\n'        \
               'VGG	19	2014\n'         \
               'VGG	16-4x pruned	2017\n' \
               'Inception	v1	2014\n'

    assert table.serialize() == expected
