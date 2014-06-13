import json

def _fix_unicodes_r(obj):
	if isinstance(obj, dict):
		for key, value in obj.items():
			if isinstance(value, unicode):
				value = str(value)
				obj[key] = value
			elif isinstance(value, dict):
				_fix_unicodes_r(value)
			if isinstance(key, unicode):
				del obj[key]
				obj[str(key)] = value

def json_load_no_unicode(*args, **kwargs):
	obj = json.load(*args, **kwargs)
	_fix_unicodes_r(obj)
	return obj

def json_loads_no_unicode(*args, **kwargs):
	obj = json.loads(*args, **kwargs)
	_fix_unicodes_r(obj)
	return obj