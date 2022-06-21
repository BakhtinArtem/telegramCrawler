setup:
	pipenv install

run_venv:
	pipenv shell

run_py:
	python3 main.py

clear:
	pipenv uninstall --all

delete:
	pipenv --rm

update:
	pipenv update