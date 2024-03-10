.PHONY: install test debug_remote remote_debug_dep

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

remote_debug_dep:
	pip install debugpy

debug_remote: install remote_debug_dep
	python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0 -p 5000

test:
	coverage run --source=src/ -m unittest discover -v

docker_build:
	docker build -t scraped-tvtime .

docker_run: docker_build
	docker run -p 8000:5000 scraped-tvtime