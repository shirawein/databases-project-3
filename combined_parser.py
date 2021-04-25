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
# print(first_word)
second_word = str(opts.vars[1]).lower()
# print(second_word)

lowered = [element.lower() for element in opts.vars]


if(first_word == "create" and second_word == "table"):
	datatype_list = []
	colname_list = []
	primary_key_list = []

	table_name = opts.vars[2]

	if len(opts.vars) > 3 and opts.vars[3] == '(':
		# print("len ", len(opts.vars[4:]))
		i = 4
		while i < len(opts.vars):
			# print("i: ", opts.vars[i])
			if opts.vars[i] == ')':
				break
			if opts.vars[i] != ')' :
				if(opts.vars[i] == "primary"):
					after_primary = opts.vars[i+3:]
					j = 0
					while j < len(after_primary):
						if after_primary[j] == ')':
							break
						if after_primary[j] != ')' :
							primary_key_list.append(after_primary[j])
							j += 1
					break
				else:
					colname_list.append(opts.vars[i])
					i += 1
					datatype_list.append(opts.vars[i])
					i += 1

	final_primary = []
	for item in primary_key_list:
		result = item.rstrip(',')
		final_primary.append(result)

	final_datatype = []
	for item in datatype_list:
		result = item.rstrip(',')
		final_datatype.append(result)

	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)	

			
	# print(table_name)
	# print(colname_list)
	# print(datatype_list)
	# print(final_primary)

	cutil._create_table(table_name, 0, len(final_colname), final_datatype, final_colname, final_primary)


if(first_word == "drop" and second_word == "table"):
	table_name = opts.vars[2]
	print(table_name)
	cutil._drop_table(table_name)

if(first_word == "select"):
	joinval = 0
	colname_list = []
	view_colname_list = []
	condition_list = []
	value_list = []
	mmcas_list = []
	andor = ""
	mmcas_operations = ["max","min","count","sum","avg"]

	table1_col_list = []
	table2_col_list = []
	table_name2 = ""
	mathcols = []
	matchcol_table1 = ""
	matchcol_table2 = ""
	join_type = ""

	f_index = lowered.index('from') 
	table_name = opts.vars[f_index+1]
	table_name_list = []
	table_name_list.append(table_name)

	before_from = opts.vars[1:f_index]
	element = 0
	while element < len(before_from):
		if before_from[element].lower() in mmcas_operations:
			mmcas_list.append(before_from[element].lower())
			element += 2
			view_colname_list.append(before_from[element])
			element += 2
		else:
			view_colname_list.append(before_from[element])
			element += 1
	# view_colname_list.append(opts.vars[f_index-1])
	if (len(opts.vars) > (f_index+2) and opts.vars[f_index+2] == 'where'):
		i = f_index+3
		while i < (len(opts.vars)):
			if opts.vars[i] == "and":
				i += 1
				andor = "and"
				continue
			if opts.vars[i] == "or":
				i += 1
				andor = "or"
				continue
			if opts.vars[i] != ')' :
				colname_list.append(opts.vars[i])
				condition_list.append(opts.vars[i+1])
				value_list.append(opts.vars[i+2])
				i = i + 3
	elif (len(opts.vars) > (f_index+3) and opts.vars[f_index+3] == 'join'):
		join_type = (opts.vars[f_index+2]).lower()
		table_name2 = opts.vars[f_index+4]
		table_name_list.append(table_name2)
		joinval = 1
		mathcols.append(opts.vars[f_index+6])
		mathcols.append(opts.vars[f_index+8])

	updated_view_colname_list = []

	for item in view_colname_list:
		result = item.rstrip(',')
		updated_view_colname_list.append(result)
			
	# print("table name ", table_name)
	# print("updated view ", updated_view_colname_list)
	# print("mmcas list ", mmcas_list)
	# print("colname ", colname_list)
	# print("condition ", condition_list)
	# print("value ", value_list)
	# print("andor ", andor)

	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)

	final_view_colname = []
	for item in updated_view_colname_list:
		result = item.rstrip(',')
		final_view_colname.append(result)

	final_value = []
	for item in value_list:
		result = item.rstrip(',')
		final_value.append(result)

	print("colname : " , final_view_colname)

	for item in final_view_colname:
		result = item.rstrip(',')
		stripped = ""
		if '.' in result:
			stripped = result.split('.')[1]
		if result.startswith(table_name):
			table1_col_list.append(stripped)
		elif result.startswith(table_name2):
			table2_col_list.append(stripped)

	print("matchcols : ", mathcols)

	for item in mathcols:
		result = item.rstrip(';')
		stripped = ""
		if '.' in result:
			stripped = result.split('.')[1]
		if result.startswith(table_name):
			matchcol_table1 = stripped
		elif result.startswith(table_name2):
			matchcol_table2 = stripped

	if joinval == 0:
		cutil._select(table_name, final_view_colname, mmcas_list, final_colname, condition_list, final_value, andor)
	if joinval == 1:
		# print(table_name_list)
		# print(table1_col_list)
		# print(table2_col_list)
		# print(matchcol_table1)
		# print(matchcol_table2)
		# print(join_type)
		cutil._join(table_name_list, table1_col_list, table2_col_list, matchcol_table1, matchcol_table2, join_type, 'off')




if(first_word == "insert" and second_word == "into"):
	colname_list = []
	value_list = []
	table_name = opts.vars[2]
	v_index = lowered.index('values')
	if opts.vars[3] == '(':
		for arg in opts.vars[4:v_index-2]:
			if arg != ')':
				colname_list.append(arg)
		colname_list.append(opts.vars[v_index-2])

	if opts.vars[v_index+1] == '(':
		for arg in opts.vars[v_index+2:-2]:
			if arg != ')':
				value_list.append(arg)
		value_list.append(opts.vars[-2])

	# print(table_name)
	# print(colname_list)
	# print(value_list)

	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)

	final_value = []
	for item in value_list:
		result = item.rstrip(',')
		final_value.append(result)	

	cutil._insert(table_name, final_colname, final_value)


if(first_word == "delete" and second_word == "from"):
	table_name = opts.vars[2]
	colname_list = []
	value_list = []
	condition_list = []
	if (len(opts.vars) > 3 and opts.vars[3] == 'where'):
		i = 4
		while i < len(opts.vars):
			if opts.vars[i] != ')' :
				if opts.vars[i] == "and":
					i += 1
					andor = "and"
					continue
				if opts.vars[i] == "or":
					i += 1
					andor = "or"
					continue
				colname_list.append(opts.vars[i])
				condition_list.append(opts.vars[i+1])
				value_list.append(opts.vars[i+2])
				i = i + 3

	# print(table_name)
	# print(colname_list)
	# print(condition_list)
	# print(value_list)

	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)

	final_value = []
	for item in value_list:
		result = item.rstrip(',')
		final_value.append(result)	

	cutil._delete(table_name, final_colname, condition_list, final_value)

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
	if opts.vars[2] == "set":
		# if where_index == 0:
		# 	for i in range(0,len(opts.vars),3):
		# 		update_colname_list.append(opts.vars[i])
		# 		condition_list.append(opts.vars[i+1])
		# 		update_value_list.append(opts.vars[i+2])
		# elif where_index != 0:
		before_where = opts.vars[3:where_index]
		after_where = opts.vars[where_index+1:]
		i = 0
		while i < len(before_where):
			update_colname_list.append(before_where[i])
			i = i + 2
			update_value_list.append(before_where[i])
			i = i + 1

		j = 0
		while j < len(after_where):
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
				j = j + 3

	# print(table_name)
	# print(update_colname_list)
	# print(update_value_list)
	# print(colname_list)
	# print(condition_list)
	# print(value_list)
	# print(andor)

	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)

	final_value = []
	for item in value_list:
		result = item.rstrip(',')
		final_value.append(result)	

	final_view_colname = []
	for item in update_colname_list:
		result = item.rstrip(',')
		final_view_colname.append(result)

	final_view_value = []
	for item in update_value_list:
		result = item.rstrip(',')
		final_view_value.append(result)	

	cutil._update(table_name, final_view_colname, final_view_value, final_colname, condition_list, final_value, andor)


if(first_word == "create" and second_word == "index"):
	index_name = opts.vars[2]
	table_name = opts.vars[4]
	after_table = opts.vars[5:]
	colname_list = []
	for item in range(0,len(after_table)):
		if after_table[item] != '(' and after_table[item] != ')':
			colname_list.append(after_table[item])


	# print(colname_list)
	final_colname = []
	for item in colname_list:
		result = item.rstrip(',')
		final_colname.append(result)

	# only supporting one column name
	colname = colname_list[0]
	
	cutil._create_index(index_name, table_name, colname)


if(first_word == "drop" and second_word == "index"):
	drop = opts.vars[2]
	table_name = drop.split('.')[0]
	index_name = drop.split('.')[1]

	cutil._drop_index(table_name, index_name)

if(first_word == "bulk" and second_word == "insert"):
	table_name = opts.vars[2]
	colnames = []
	colnames.append("one")
	colnames.append("two")
	# datatypes = []
	# datatypes.append("int")
	# datatypes.append("int")
	# primary_keys = []
	# primary_keys.append("one")

	# cutil._create_table(table_name, 0, len(colnames), datatypes, colnames, primary_keys)

	if table_name == "Rel-i-i-1000":
		for item in range(1,1001):
			values = []
			values.append(item)
			values.append(item)
			cutil._insert(table_name, colnames, values)

	if table_name == "Rel-i-1-1000":
		for item in range(1,1001):
			values = []
			values.append(item)
			values.append(1)
			cutil._insert(table_name, colnames, values)

	if table_name == "Rel-i-i-10000":
		for item in range(1,10001):
			values = []
			values.append(item)
			values.append(item)
			cutil._insert(table_name, colnames, values)

	if table_name == "Rel-i-1-10000":
		for item in range(1,10001):
			values = []
			values.append(item)
			values.append(1)
			cutil._insert(table_name, colnames, values)

	if table_name == "Rel-i-i-100000":
		for item in range(1,100001):
			values = []
			values.append(item)
			values.append(item)
			cutil._insert(table_name, colnames, values)

	if table_name == "Rel-i-1-100000":
		for item in range(1,100001):
			values = []
			values.append(item)
			values.append(1)
			cutil._insert(table_name, colnames, values)

