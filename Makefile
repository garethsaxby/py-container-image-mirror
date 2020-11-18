init:
	pipenv install

lint:
	pipenv run black --check cim.py
	pipenv run isort -c cim.py
	pipenv run pylint cim.py