.PHONY: install test

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	coverage run --source=src/ -m unittest discover -v