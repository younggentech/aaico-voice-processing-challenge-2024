CODE_FOLDERS := src
TEST_FOLDER := tests
.PHONY: test format lint

test:
	poetry run pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS)

format:
	poetry run black --line-length 79 $(CODE_FOLDERS)

lint:
	poetry run black --line-length 79 --check $(CODE_FOLDERS) $(TEST_FOLDER)
	poetry run flake8 $(CODE_FOLDERS) $(TEST_FOLDER)
	poetry run ruff check $(CODE_FOLDERS) $(TEST_FOLDER)
