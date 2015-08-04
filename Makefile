version := $(shell python setup.py --version)

clean:
	rm -f */*.pyc
	rm -rf dist/
	rm -rf *.egg-info/

test:
	./setup.py test

build: test
	./setup.py sdist

upload:
	./setup.py sdist upload
