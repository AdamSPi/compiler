all: setup

test:
	pytest

setup:
	python3 -m venv venv/
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	
clean:
	rm -rf venv/ .pytest_cache/ __pycache__/
