install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest tests/* -vv

coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/*

local-coverage:
	poetry run pytest --cov=page_loader tests/*
