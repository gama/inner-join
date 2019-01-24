import fileinput
import innerjoin


def main():
    lines = [line for line in fileinput.input()]
    try:
        parsed_query = innerjoin.Parser.parse(''.join(lines))
        input_tables = innerjoin.Loader.load(parsed_query)
        output_table = innerjoin.Joiner.join(input_tables, parsed_query)
        output_table.print()
    except innerjoin.InvalidSyntaxError:
        print('invalid syntax')
    except innerjoin.MissingTableError:
        print('missing table')
    except innerjoin.InvalidTableError:
        print('invalid table')
    except innerjoin.InvalidFieldError:
        print('invalid field')
    except innerjoin.DuplicateFieldError:
        print('duplicate field')
