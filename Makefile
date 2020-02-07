all: setup

test:
	python3 test_r0.py < test_r0.input

setup:
	python3 -m venv venv/
	source venv/bin/activate; \
	pip install -r requirements; \
	
clean:
	rm -rf venv/