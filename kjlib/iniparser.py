import os, re

_RE_BLOCK = "^\s*\[([^]]+)\]\s*$"

class IniParser:
	@staticmethod
	def parse(filePath):
		if not os.path.exists(filePath):
			raise ValueError("%s does not exist." % filePath)
		with open(filePath, "r") as f:
			content = f.read()
		d = {}
		content = re.split(_RE_BLOCK, content, 0, re.MULTILINE)[1:]
		sections = zip(content[0::2], content[1::2])
		for sectionName, sectionContent in sections:
			dd = {}
			lines = sectionContent.strip().split("\n")
			lines = [line.strip().split("=", 1) for line in lines]
			for pair in lines:
				key = pair[0].strip()
				value = pair[1].strip() if len(pair) > 1 else None
				dd[key] = value
			d[sectionName] = dd
		return d

	@staticmethod
	def merge(dictOld, dictNew):
		for section in dictNew:
			if section not in dictOld:
				dictOld[section] = {}
			for pair in dictNew[section].iteritems():
				key = pair[0]
				value = pair[1] if len(pair) > 1 else None
				dictOld[section][key] = value
