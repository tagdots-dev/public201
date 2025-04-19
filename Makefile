# NOTE: this file is managed by terraform
# Makefile

usage:
	@echo "Usage:"
	@echo "\tmake build"
	@echo "\tmake test"

build:
	@echo
	@echo "***************************************************************************"
	@echo "******************* Upgrade to the latest python build ********************"
	@echo "***************************************************************************"
	@echo
	python -m pip install -U build

	@echo
	@echo "***************************************************************************"
	@echo "******************** Build software package *******************************"
	@echo "***************************************************************************"
	@echo
	python -m build

	@echo
	@echo "***************************************************************************"
	@echo "****** Install package into the current active Python environment *********"
	@echo "***************************************************************************"
	@echo
	python -m pip install -e .

test:
	@echo
	@echo "***************************************************************************"
	@echo "************************* Running coverage tests **************************"
	@echo "***************************************************************************"
	@echo
	coverage run -m unittest -v
	coverage html
	coverage report -m

.PHONY: help build test
