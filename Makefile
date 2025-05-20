install:
    uv pip install --upgrade pip
    uv pip install .

test:
    uv pip install pytest
    uv pip run pytest -vv --cov= test_*. 

format:	
    uv pip install black
    uv pip run black .

lint:
    uv pip install ruff
    uv pip run ruff check --fix .
    uv pip run ruff check .

deploy:
    # no rules for now
        
all: install lint test format