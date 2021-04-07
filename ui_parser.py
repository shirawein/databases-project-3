## Databases project 3

# myls.py
# Import the argparse library
import argparse

import os
import sys

parser = argparse.ArgumentParser(description='List the content of a folder')

parser.add_argument('vars', nargs='+')
opts = parser.parse_args()	

print(opts)

# def add_table():
# 	my_parser.add_argument('a', help='a first argument')

# 	my_parser.add_argument('a', help='a first argument')


# my_parser.add_argument('-v',
#                        '--verbose',
#                        action='store_true',
#                        help='an optional argument')

# # Execute parse_args()
# args = my_parser.parse_args()

# print('If you read this line it means that you have provided '
#       'all the parameters')

# # Create the parser

# # Add the arguments
# my_parser.add_argument('Operation',
#                        metavar='Operation',
#                        type=str,
#                        help='create_table, drop_table, create_index, drop_index, select, insert, delete, update')

# # Execute the parse_args() method
# args = my_parser.parse_args()

# operation = args.Operation

# types_of_operations = ["create_table", "drop_table", "create_index", "drop_index", "select", "insert", "delete", "update"]

# if not operation in types_of_operations:
#     print(' The operation must be one of the following: "create_table", "drop_table", "create_index", "drop_index", "select", "insert", "delete", "update" ')
#     sys.exit()

# if operation is "create_table":
# 	my_parser.add_table()




