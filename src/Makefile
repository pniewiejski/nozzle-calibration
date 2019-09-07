install:
	pip3 install -r requirements.txt 
cleanup:
	find . | grep -E "(__pycache__$$|.pytest_cache$$)" | xargs rm -r
format:
	black . -l 125
run: 
	python3 -m data_exploring.new-approach
