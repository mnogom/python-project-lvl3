install:
	poetry install

gen-diff:
	poetry run gendiff

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest tests/tests.py -vv

coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/tests.py

local-coverage:
	poetry run pytest --cov=page_loader tests/tests.py

page_load_test:
	poetry run page-loader
