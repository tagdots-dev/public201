# Makefile

usage:
	@echo "Usage:"
	@echo "\tmake build"

build:
	@echo
	@echo " *************************************************************************** "
	@echo " ******************* Upgrade to the latest python build ******************** "
	@echo " *************************************************************************** "
	@echo
	python -m pip install -U build

	@echo
	@echo " *************************************************************************** "
	@echo " ******************** Build software package ******************************* "
	@echo " *************************************************************************** "
	@echo
	python -m build

	@echo
	@echo " *************************************************************************** "
	@echo " ****** Install package into the current active Python environment ********* "
	@echo " *************************************************************************** "
	@echo
	python -m pip install -e .

.PHONY: help build
