## Databases project 3

# myls.py
# Import the argparse library
import argparse

import os
import sys

import sqlparse


def sql_parser(query):
	parsed = sqlparse.parse(query)[0]
	return parsed.tokens

parser = argparse.ArgumentParser(description='List the content of a folder')

parser.add_argument('vars', nargs='+')
opts = parser.parse_args()	

# print(opts.vars)

all_input = ' '.join(opts.vars)

# print(all_input)

print(sql_parser(all_input))
