A toy solution for formatted data dumper, checkout file_parser.md for problem description.

## Run data dumper:

```
virtualenv .venv
. .venv/bin/activate
make prepare
python main.py sqlite:///:memory: test_table tests/data/simple_format_2015-06-28.txt
```

## Run tests:

```
make test
```
