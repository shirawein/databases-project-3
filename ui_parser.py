## Databases project 3

# myls.py
# Import the argparse library
import argparse

import os
import sys

parser = argparse.ArgumentParser(description='List the content of a folder')

parser.add_argument('vars', nargs='+')
opts = parser.parse_args()	

print(opts.vars)

all_input = ' '.join(opts.vars)

print(all_input)
#all_input is what should then be passed into the sql_parser
