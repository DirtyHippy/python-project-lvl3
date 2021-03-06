install:
	poetry install

loader:
	poetry run page-loader

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader
	poetry run mypy page_loader

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
