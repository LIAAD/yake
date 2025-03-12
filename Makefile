install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest --nbval *.ipynb
	python -m pytest -vv --cov= test_*.py

format:	
	black *.py 

lint:
	ruff check *.py

deploy:
	# no rules for now
		
all: install lint test format