import csv
import os

def _init_storage():
	with open("table_data.csv", 'a', newline='') as file:
		writer = csv.writer(file, delimiter = ",")
		writer.writerow(["table_name", "nrows", "ncols", "datatype_list"])

def _create_table(table_name, nrows, ncols, datatype_list, colname_list):
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
		writer.writerow([table_name, nrows, ncols, datatype_list])

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
		

_init_storage()
_create_table("table3", 0, 3, ['int', 'char', 'char'], ['id', 'name', 'company'])
_drop_table("table3")