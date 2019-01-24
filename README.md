## Inner join

Conceptually, a table is a finite collection of N records (rows), where each row
is a tuple x = (x 1 , . . . , x K ), whose K fields (columns) are associated
with names (f i , . . . , f K ). An inner join is an operation that takes two
tables with N a and N b rows, respectively, and produces a table with N c ≤ N a
× N b rows. Conceptually, each row of the output table is determined by taking a
row i and a row j from the two input tables, respectively, and selecting a
subset of their columns. Optionally, the rows of the output table may be
filtered, so that the output table contains only a subset of the N a × N b rows.
In the special case considered here, the filter condition is an equality
comparison between a subset of the fields.

#### Problem

Your task is to write a program that parses a description of the inner join
query, loads the two tables, and produces the output of the inner join. The
primary criterion is the correctness of the output. The secondary criterion is
the computational complexity, as judged by reading your code. We will also
evaluate the clarity of the code you produce.

**Input / output format**

Your program should read the join specification from standard input, load the
two tables from the corresponding files in the current directory, and write the
resulting table to the standard output.

**Input query**

The input specification will conform to the SQL standard. It is a string
  `SELECT <output_spec> FROM <a> INNER JOIN <b> [ON <condition>]`
where:

* `<a>` and `<b>` are the identifiers of table names with `<a>` 6 = `<b>` (no
  self-joins);
* `<output_spec>` consists of comma-separated field descriptors `<table>.<field>` AS
  `<name>`, where `<table>` is the identifier listed in either `<a>` or `<b>`, the
  identifier `<field>` is the name of the field in the corresponding table file
  (see below), and `<name>` is a unique identifier of the output field;
* `<condition>` consists of AND-separated equality comparison, where each
  comparison is of the form `<table1>.<field1>` = `<table2>.<field2>`, exactly one
  of `<table1>`, `<table2>` is `<a>` and the other one is `<b>`, and <field1> and
  `<field2>` are the field names in the table <table1> and `<table2>`, respectively.
  Note that the ON portion of the query is optional.

All table and field identifiers start with a letter and consist entirely of
letters and digits. None of the identifiers are case-sensitive, and neither are
the keywords SELECT, FROM, INNER, JOIN, ON, and AND. The valid whitespace
characters are “ \t\r\n\f”.

**Input files** Both tables reside in the current directory with filenames
matching the lower-case table name with extension `.tsv`. The first line consists
of tab-separated field names. The subsequent lines consist of tab-separated
field values. The value can be any string not containing a tab or end-
of-the-line characters.

**Output** If the input query is valid, the resulting table must be written to
the standard output in the format described in the previous paragraph (the rows
can be ordered arbitrarily). Otherwise, print out a single line with one of the
following error descriptions:

* invalid syntax: the query does not match the above syntax or uses invalid identifiers;
* missing table: a table specified in the query was not found in the current directory;
* invalid table: a referenced table does not match the ones provided in FROM / INNER JOIN;
* invalid field: a referenced field was not found in the corresponding table;
* duplicate field: the field names in the output table are not unique.

You can assume that the input tables have the correct format if they exist.

Please pay special attention to the format of the output (e.g., no debugging
information, no extra spaces at the end of the line, no additional lines at the
end). The correctness of your solution will be evaluated programmatically, and
we may reject solutions that do not conform to this specification. Use stderr
for any debugging output.

**Example**
Consider the following two tables, nets and perf (horizontal lines added here for legibility):

| Network   | Version      | Year |
|-----------|--------------|------|
| VGG       | 19           | 2014 |
| VGG       | 16-4x pruned | 2017 |
| Inception | v1           | 2014 |

| Network     | Version | Dataset     | ErrorRate |
|-------------|---------|-------------|-----------|
| VGG         | 19      | ImageNet    | 7.32      |
| VGG         | 19      | Caltech-256 | 14.9      |
| Inception   | v1      | ImageNet    | 6.67      |
| SuperVision | ?       | ImageNet    | 16.4      |

Given the following query

```
SELECT
  nets.version AS version,
  nets.year AS published,
  perf.dataset AS dataset,
  perf.errorrate AS errors
FROM nets
INNER JOIN perf
ON nets.network=perf.network AND nets.version = perf.version
```

the output table is

|version | published | dataset     | errors |
|--------|-----------|-------------|--------|
| 19     | 2014      | ImageNet    | 7.32   |
| 19     | 2014      | Caltech-256 | 14.9   |
| v1     | 2014      | ImageNet    | 6.67   |


## Installation

```
pip3 -m virtualenv venv/
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .
```


## Running

```
$EDITOR table1.tsv
$EDITOR table2.tsv
echo "SELECT ... FROM table1 INNER JOIN table2 ..." | ./innerjoiner
```
