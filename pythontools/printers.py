from collections import OrderedDict

def printTable(matrix, printHeader=False, printRowId=False):
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
		print template % matrix[0]
		print "-" * (sum([x + 2 for x in widths.itervalues()]))
		matrix = matrix[1:]
	for line in matrix:
		print template % line
