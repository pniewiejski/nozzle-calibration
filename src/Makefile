install:
	pip3 install -r requirements.txt 
install-all:
	pip3 install -r requirements.txt;\
	pip3 install -r requirements-dev.txt 
cleanup:
	find . | grep -E "(__pycache__$$|.pytest_cache$$)" | xargs rm -r
format:
	black . -l 125
run: 
	python3 -m data_exploring.check_balance
