# Setup
###
target=$(PWD)/build
source=$(PWD)/src

pypath=PYTHONPATH=$(target):./maxcdn:$(PYTHONPATH)

nose_opts=-v
nose=python $(source)/nose/bin/nosetests
cov_opts= --with-coverage --cover-package=maxcdn

benchmark=./test/benchmark.py
tests=./test/test.py
int=./test/int.py

# Tasks
###
init: clean setup test

setup: distribute
	pip install -r requirements.txt -t $(target) -b $(source)

console:
	$(pypath) python

clean:
	rm -rf $(source) $(target) .ropeproject .coverage junit-report.xml
	find . -type f -name "*.pyc" -exec rm -v {} \;

coverage: build/coverage
	$(pypath) python $(nose) $(cov_opts) $(tests)

benchmark:
	$(pypath) python $(benchmark)

test:
	$(pypath) python $(tests)

test/2:
	# python 2.x
	$(pypath) python2 $(tests)

test/32:
	# python 3.2
	$(pypath) python3.2 $(tests)

test/33:
	# python 3.3
	$(pypath) python3.3 $(tests)

test/all:
	-make test/2
	-make test/32
	-make test/33

nose: build/nose
	$(pypath) $(nose) $(nose_opts) $(tests)

nose/int: build/nose
	$(pypath) $(nose) $(nose_opts) $(int)

nose/all: nose nose/int

int:
	$(pypath) python $(test_opts) $(int)

int/2:
	# python 2.x
	$(pypath) python2 $(test_opts) $(int)

int/32:
	# python 3.2
	$(pypath) python3.2 $(test_opts) $(int)

int/33:
	# python 3.3
	$(pypath) python3.3 $(test_opts) $(int)

int/all:
	-make int/2
	-make int/32
	-make int/33

travis: setup test

distribute:
	pip install distribute

build/coverage:
	pip install coverage -t $(target) -b $(source)

build/nose:
	pip install nose -t $(target) -b $(source)

readme:
	pandoc -s -t rst --toc README.md -o tmp.text
	cat tmp.text| grep -v "Build\|Status" > README.text
	rm tmp.text

upload: readme
	python setup.py sdist register upload

.PHONY: init clean test coverage test/help test/32 test/33
