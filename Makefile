.PHONY:

clean: clean_pyc

clean_pyc:
	find . -name "*.pyc" -delete

dependencies:
	pip install -r ./requirements.txt

test:
	python `which nosetests` tests  -s --pdb

test_main:
	python main.py sqlite:///:memory: test_table tests/data/simple_format_2015-06-28.txt
