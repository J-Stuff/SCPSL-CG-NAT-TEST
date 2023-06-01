@REM This program quickly updates PDM to use the requirements.txt file. Not needed for running the program, just a script to make developing it easier
@echo off
pdm import -f requirements requirements.txt
pdm export -f requirements -o ./requirements.txt --without-hashes
pdm update
EXIT