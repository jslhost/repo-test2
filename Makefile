SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: clean 

pipeline: data/clean_dataset.csv
	
data:
	mkdir data

data/raw_dataset.csv: | data
	python -m src.load_data

data/clean_dataset.csv: data/raw_dataset.csv
	python -m src.clean_data

clean:
	rm -r data