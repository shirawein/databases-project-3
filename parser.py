## Databases project 3

# myls.py
# Import the argparse library
import argparse

import os
import sys

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('Operation',
                       metavar='Operation',
                       type=str,
                       help='create_table, drop_table, create_index, drop_index, select, insert, delete, update')

# Execute the parse_args() method
args = my_parser.parse_args()

operation = args.Operation

types_of_operations = ["create_table", "drop_table", "create_index", "drop_index", "select", "insert", "delete", "update"]

if not operation in types_of_operations:
    print(' The operation must be one of the following: "create_table", "drop_table", "create_index", "drop_index", "select", "insert", "delete", "update" ')
    sys.exit()

print('\n'.join(os.listdir(input_path)))
