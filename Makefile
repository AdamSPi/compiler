all: setup

test:
	pytest

setup:
	python3 -m venv venv/
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	
build:
# 	as asm/double.asm -o asm/double.o
# 	ld -e _main -macosx_version_min 10.10 -lSystem -arch x86_64 asm/double.o -o asm/dbl.out
	gcc -g runtime.c x.s -o x.bin

clean:
	rm -rf venv/ .pytest_cache/ __pycache__/ *.out
