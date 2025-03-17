install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	# python -m pytest --nbval *.ipynb
	python -m pytest -vv --cov= test_*.py

format:	
	black .

lint:
	ruff check --fix .
	ruff check .

deploy:
	# no rules for now
		
all: install lint test format
