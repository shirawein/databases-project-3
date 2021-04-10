import csv
import os
import re

def merge(list1, list2):
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def get_loc(colname, colname_list):
	i = -1
	for col in colname_list:
		i += 1
		if colname == col:
			return(i)

def condition_function(obj1, sign, obj2):
	if sign == '=':
		if obj1 == obj2:
			return True
	elif sign == '<':
		if obj1 < obj2:
			return True
	elif sign == '>':
		print(obj1)
		print(obj2)
		print(obj1 > obj2)
		if obj1 > obj2:
			return True
	elif sign == '<=':
		if obj1 <= obj2:
			return True
	elif sign == '>=':
		if obj1 >= obj2:
			return True
	return False

def _init_storage():
	with open("table_data.csv", 'a', newline='') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(["table_name", "nrows", "ncols", "datatype_list", "primary_key_list"])

def _create_table(table_name, nrows, ncols, datatype_list, colname_list, primary_key_list):
	with open('table_data.csv') as file:
		# check for duplicates
		csv_reader = csv.reader(file, delimiter=',')
		for row in csv_reader:
			# print(row)
			if row[0] == table_name:
				print("Duplicate entry, cannot create table")
				return
		
		# if no duplicates found write
	with open('table_data.csv', 'a') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow([table_name, nrows, ncols, datatype_list, primary_key_list])

	file_name = table_name + ".csv"
	with open(file_name, 'w') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerows([colname_list])

def _drop_table(table_name):
	
	file_name= table_name + ".csv"

	# check if table exists 
	lines = list()
	flag = 0
	with open('table_data.csv', 'r') as readFile:
	    reader = csv.reader(readFile)
	    for row in reader:
	        if row[0] == table_name:
	        	flag = 1
	        else:
		        lines.append(row)
	with open('table_data.csv', 'w') as writeFile:
	    writer = csv.writer(writeFile)
	    writer.writerows(lines)

	if flag == 1:
		if os.path.exists(file_name):
		    os.remove(file_name)
		    print("The table: {} is deleted!".format(table_name))
		else:
		    print("The table: {} does not exist!".format(table_name))
	else:
		print("The table: {} does not exist!".format(table_name))

def _insert(table_name, colname_list, value_list):

	file_name = table_name + ".csv"

	#  check if table_name exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				primary_key_list = row[-1]
				# primary_key_list = re.findall('"([^"]*)"', primary_key_list)
				primary_key_list = re.findall("'([^']*)'", primary_key_list)
				# print(primary_key_list)
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
	    print("The table: {} does not exist!".format(table_name))
	    return

	# check for uniqueness of primary key
	with open(file_name, 'r') as readFile:
	    reader = csv.reader(readFile)
	    for row in reader:
	    	sorted_colname_list = row
	    	break

	primary_key_loc = []
	for pk in primary_key_list:
		i = -1
		for col in sorted_colname_list:
			i += 1
			if pk == col:
				primary_key_loc.append(i)

	tuple_list = merge(colname_list, value_list)
	sorted_tuple_list = [tuple for x in sorted_colname_list for tuple in tuple_list if tuple[0] == x]

	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			count = 0
			for i in primary_key_loc:
				if str(sorted_tuple_list[i][1]) == row[i]:
					count += 1
					if count == len(primary_key_list):
						print("Entry with the same primary key exist")
						return

	# write
	with open(file_name, 'a') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(list(map(list, zip(*sorted_tuple_list)))[1])

def _delete(table_name, colname_list, condition_list, value_list):
	
	file_name= table_name + ".csv"

	# check if table exists
	flag = 0
	with open('table_data.csv') as readFile:
		reader = csv.reader(readFile, delimiter=',')
		for row in reader:
			if row[0] == table_name:
				flag = 1
				break
	if flag == 0 or not os.path.exists(file_name):
		print("The table: {} does not exist!".format(table_name))
		return

	# get the sorted complete col names
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		for row in reader:
			sorted_colname_list = row
			break	

	lines = list()
	with open(file_name, 'r') as readFile:
		reader = csv.reader(readFile)
		first_row = True
		for row in reader:
			true_flag = 0
			if(not first_row):
				for i in range(0, len(colname_list)):
					loc = get_loc(colname_list[i], sorted_colname_list)
					if not condition_function(row[i], condition_list[i], str(value_list[i])):
						true_flag = 1
			else:
				first_row = False
				true_flag = 1
			if true_flag == 1:
				lines.append(row)

	with open(file_name, 'w') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerows(lines)


#_init_storage()
#_drop_table('table_name_test')
#_create_table('table_name_test', 0, 2, ['int', 'varchar 20'], ['idd', 'namee'], ['idd', 'namee'])
#_insert('table_name_test', ['idd', 'namee'], [10, 'asdf'])
_delete('table_name_test', ['idd', 'namee'], ['>', '='], [12, 'asdf'])














