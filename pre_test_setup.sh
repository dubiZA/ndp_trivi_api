#!/bin/bash

dropdb trivia
createdb trivia
psql trivia < ./backend/trivia.psql
python ./backend/test_flaskr.py