# myls.py
# Import the argparse library
import argparse

import os
import sys

import sqlparse

from csv_util import *

def sql_parser(query):
	parsed = sqlparse.parse(query)[0]
	return parsed.tokens

parser = argparse.ArgumentParser(description='List the content of a folder')

parser.add_argument('vars', nargs='+')
opts = parser.parse_args()	

# print(opts.vars)

# all_input = ' '.join(opts.vars)

# print(all_input)

#parse first word
first_word = str(opts.vars[0]).lower()
print(first_word)
second_word = str(opts.vars[1]).lower()
print(second_word)

if(first_word == "create" and second_word == "table"):
	datatype_list = []
	colname_list = []

	table_name = opts.vars[2]
	print(table_name)

	if opts.vars[3] == '(':
		print("len ", len(opts.vars[4:]))
		for i in range(4,len(opts.vars),2):
			print("i: ", i)
			if opts.vars[i] is not ')' :
				colname_list.append(opts.vars[i])
				datatype_list.append(opts.vars[i+1])
				
			
	# print(table_name)
	# print(0)
	# print(len(colname_list))
	# print(datatype_list)
	# print(colname_list)
	_create_table(table_name, 0, len(colname_list), datatype_list, colname_list)


#print(sql_parser(all_input))

