version := $(shell python setup.py --version)

clean:
	rm -f */*.pyc
	rm -rf dist/
	rm -rf *.egg-info/

build:
	./setup.py sdist

upload:
	./setup.py sdist upload
