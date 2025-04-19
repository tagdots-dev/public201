# NOTE: this file is managed by terraform
# Makefile

usage:
	@echo "Usage:"
	@echo "\tmake build"
	@echo "\tmake test"

build:
	@echo "***************************************************************************"
	@echo "******************* Upgrade to the latest python build ********************"
	@echo "***************************************************************************"
	python -m pip install -U build

	@echo "***************************************************************************"
	@echo "******************** Build software package *******************************"
	@echo "***************************************************************************"
	PYTHONWARNINGS=error python -m build

	@echo "***************************************************************************"
	@echo "****** Install package into the current active Python environment *********"
	@echo "***************************************************************************"
	python -m pip install -e .

test:
	@echo "***************************************************************************"
	@echo "************************* Running coverage tests **************************"
	@echo "***************************************************************************"
	coverage run -m unittest -v

	@echo "\n"
	@echo "## Create an HTML report of the coverage of the files"
	coverage html

	@echo "\n"
	@echo "## Report coverage statistics on modules"
	coverage report -m

.PHONY: help build test
