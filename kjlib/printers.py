from collections import OrderedDict

def formatTable(matrix, printHeader=False, printRowId=False):
	table_str = ""
	widths = OrderedDict()
	for lineNum in xrange(len(matrix)):
		for colNum in xrange(len(matrix[lineNum])):
			if colNum not in widths:
				widths[colNum] = 0
			widths[colNum] = max(widths[colNum], len(matrix[lineNum][colNum]))
	template = "%%-%ds   " * (len(widths) - 1)
	if printRowId:
		template = "%%-%ds | " + template
	else:
		template = "%%-%ds   " + template
	template = template.strip()
	template = template % tuple(widths.values())
	if printHeader:
		table_str += template % matrix[0]
		table_str += "\n"
		table_str += ("-" * (sum([x + 3 for x in widths.itervalues()]) - 3))
		table_str += "\n"
		matrix = matrix[1:]
	for line in matrix:
		table_str += template % line
		table_str += "\n"
	table_str = table_str[:-1]
	return table_str

def format_table(matrix, print_header=False, print_row_id=False):
	return formatTable(matrix, printHeader=print_header, printRowId=print_row_id)
