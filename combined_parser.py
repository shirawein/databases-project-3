# myls.py
# Import the argparse library
import argparse

import os
import sys

import sqlparse

import csv_util as cutil

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

lowered = [element.lower() for element in opts.vars]


if(first_word == "create" and second_word == "table"):
	datatype_list = []
	colname_list = []
	primary_key_list = []

	table_name = opts.vars[2]
	print(table_name)

	if len(opts.vars) > 3 and opts.vars[3] == '(':
		# print("len ", len(opts.vars[4:]))
		for i in range(4,len(opts.vars),2):
			# print("i: ", i)
			if opts.vars[i] != ')' :
				colname_list.append(opts.vars[i])
				if(opts.vars[i+1][-1] == ','):
					datatype_list.append(opts.vars[i+1][:-1])
				else:
					if(opts.vars[i+2] == "primary"):
						datatype_list.append(opts.vars[i+1][:-1])
						primary_key_list.append(opts.vars[i+1][:-1])
						i += 2
				
	cutil._create_table(table_name, 0, len(colname_list), datatype_list, colname_list, primary_key_list)


if(first_word == "drop" and second_word == "table"):
	table_name = opts.vars[2]
	print(table_name)
	cutil._drop_table(table_name)

if(first_word == "select"):
	print(opts.vars)
	colname_list = []
	view_colname_list = []
	condition_list = []
	value_list = []
	mmcas_list = []
	andor = ""
	mmcas_operations = ["max","min","count","sum","avg"]
	f_index = lowered.index('from') 
	table_name = opts.vars[f_index+1]
	before_from = opts.vars[1:f_index]
	for element in range(0,len(before_from)):
		if before_from[element].lower() in mmcas_operations:
			mmcas_list.append(before_from[element].lower())
			element += 1
			view_colname_list.append(before_from[element])
			element += 1
		else:
			mmcas_list.append("")
			view_colname_list.append(before_from[element])
	# view_colname_list.append(opts.vars[f_index-1])
	if (len(opts.vars) > (f_index+1) and opts.vars[f_index+1] == 'where'):
		for i in range(f_index+2,len(opts.vars),3):
			if opts.vars[i] != ')' :
				if opts.vars[i] == "and":
					andor = "and"
					i += 1
				elif opts.vars[i] == "or":
					andor = "or"
					i += 1
				colname_list.append(opts.vars[i])
				condition_list.append(opts.vars[i+1])
				value_list.append(opts.vars[i+2])

	updated_view_colname_list = []

	for item in view_colname_list:
		result = item.rstrip(',')
		updated_view_colname_list.append(result)
			
	print("table name ", table_name)
	print("updated view ", updated_view_colname_list)
	print("mmcas list ", mmcas_list)
	print("colname ", colname_list)
	print("condition ", condition_list)
	print("valie ", value_list)
	print("andor ", andor)

	cutil._select(table_name, updated_view_colname_list, mmcas_list, colname_list, condition_list, value_list, andor)

if(first_word == "insert" and second_word == "into"):
	colname_list = []
	value_list = []
	table_name = opts.vars[2]
	v_index = lowered.index('values')
	if opts.vars[3] == '(':
		for arg in opts.vars[3:v_index-2]:
			if arg != ')':
				colname_list.append(arg[:-1])
		colname_list.append(opts.vars[v_index-2])
	if opts.vars[v_index+1] == '(':
		for arg in opts.vars[v_index+2:-2]:
			if arg != ')':
				value_list.append(arg[:-1])
		value_list.append(opts.vars[-2])


	cutil._insert(table_name, colname_list, value_list)


if(first_word == "delete" and second_word == "from"):
	table_name = opts.vars[3]
	colname_list = []
	value_list = []
	condition_list = []
	if (len(opts.vars) > 3 and opts.vars[4] == 'where'):
		for i in range(5,len(opts.vars),3):
			if opts.vars[i] != ')' :
				colname_list.append(opts.vars[i])
				condition_list.append(opts.vars[i+1])
				value_list.append(opts.vars[i+2])

	cutil._delete(table_name, colname_list, condition_list, value_list)


if(first_word == "update"):
	table_name = second_word
	where_index = 0
	colname_list = []
	update_colname_list = []
	value_list = []
	update_value_list = []
	condition_list = []
	andor = ""
	if 'where' in lowered:
		where_index = lowered.index('where') 
	if opts.vars[3] == "set":
		if where_index == 0:
			for i in range(0,len(opts.vars),3):
				update_colname_list.append(opts.vars[i])
				condition_list.append(opts.vars[i+1])
				update_value_list.append(opts.vars[i+2])
		elif where_index != 0:
			before_where = opts.vars[4:where_index]
			after_where = opts.vars[where_index+1:]
			for i in range(0,len(before_where),3):
				colname_list.append(before_where[i])
				condition_list.append(before_where[i+1])
				value_list.append(before_where[i+2])
			for j in range (0, after_where, 3):
				if after_where[j] != ')' :
					if after_where[j] == "and":
						andor = "and"
						j += 1
					elif after_where[j] == "or":
						andor = "or"
						j += 1
					colname_list.append(after_where[j])
					condition_list.append(after_where[j+1])
					value_list.append(after_where[j+2])

	cutil._update(table_name, update_colname_list, update_value_list, colname_list, condition_list, value_list, andor)
