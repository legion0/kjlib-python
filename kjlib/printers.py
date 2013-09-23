from collections import OrderedDict
import sys

def format_table(table_tuples, print_header=False, print_row_id=False):
	table_str = ""
	max_columns = 0
	for lineNum in xrange(len(table_tuples)):
		max_columns = max(max_columns, len(table_tuples[lineNum]))
	widths = [0] * max_columns
	for lineNum in xrange(len(table_tuples)):
		for colNum in xrange(len(table_tuples[lineNum])):
			widths[colNum] = max(widths[colNum], len(table_tuples[lineNum][colNum]))
	template = "%%-%ds   " * (len(widths) - 1)
	if print_row_id:
		template = "%%-%ds | " + template
	else:
		template = "%%-%ds   " + template
	template = template.strip()
	template = template % tuple(widths)
	if print_header:
		table_str += template % table_tuples[0]
		table_str += "\n"
		table_str += ("-" * (sum([x + 3 for x in widths]) - 3))
		table_str += "\n"
		table_tuples = table_tuples[1:]
	for line in table_tuples:
		table_str += template % line
		table_str += "\n"
	table_str = table_str[:-1]
	return table_str

def _test(args):
	header = (("Column 1", "Column 2", "Column 3"),)
	data = (
		("1", "2", "3"),
		("4", "5", "6"),
		("7", "8", "9"),
	)
	mat = header + data
	print format_table(mat)
	print "=" *60
	print format_table(mat, True)
	print "=" *60
	print format_table(mat, False, True)
	print "=" *60
	print format_table(mat, True, True)

if __name__ == '__main__':
	_test(sys.argv[1:])
