import sqlparse

def sql_parser(query):
	parsed = sqlparse.parse(query)[0]
	return parsed.tokens