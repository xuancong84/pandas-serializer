#!/usr/bin/env python3
# coding=utf-8

import os, sys, io, re, pandas, gzip, types


def Open(fn, mode='r', **kwargs):
	if fn == '-':
		return sys.stdin if mode.startswith('r') else sys.stdout
	return gzip.open(fn, mode, **kwargs) if fn.lower().endswith('.gz') else open(fn, mode, **kwargs)


class TC:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	BLR = '\033[1m\033[91m'
	BLG = '\033[1m\033[92m'
	BLY = '\033[1m\033[93m'
	LR = '\033[91m'
	LG = '\033[92m'
	LY = '\033[93m'


def makedirs(path):
	try:
		os.makedirs(path)
	except:
		pass


try:
	assert type(pandas_sep)==str and len(pandas_sep)
except:
	pandas_sep = ','

# decode pandas objects from strings if found
def pandas_decode(obj, sep=pandas_sep):
	if type(obj) == list:
		return [pandas_decode(i, sep=sep) for i in obj]
	elif type(obj) == tuple:
		return (pandas_decode(i, sep=sep) for i in obj)
	elif type(obj) == set:
		return {pandas_decode(i, sep=sep) for i in obj}
	elif type(obj) == dict:
		return {pandas_decode(k, sep=sep): pandas_decode(v, sep=sep) for k, v in obj.items()}
	elif type(obj) != str:
		return obj
	elif not obj.startswith('\0'):
		return obj
	try:
		obj1 = obj[1:]
		if obj1.startswith("<") and obj1.endswith('>'):
			rem = re.fullmatch("<([^ ]+) ([^ ]+).*>", obj1)
			obj_type, obj_name = rem.groups()
			obj1 = eval(obj_name[1:-1] if re.match("'.*'", obj_name) else obj_name)
			obj = obj1 if str(obj1).startswith('<'+obj_type+' ') else obj
		else:
			dct = eval(obj1)
			if dct['type'] in ['DataFrame', 'Series']:
				df = pandas.read_csv(io.StringIO(dct['csv']))
				df.columns = dct['csv'].splitlines()[0].split(sep)
				index_col = df.columns[:-1] if dct['type'] == 'Series' else [(df.columns[0] if c == None else c) for c in dct['index']]
				obj = df.set_index(index_col)
	except:
		pass
	return obj


# load object from string
def pandas_loads(repr, sep=pandas_sep):
	return pandas_decode(eval(repr, {'nan':float('nan')}), sep=sep)


# load object from file/filename
def pandas_load(fp, sep=pandas_sep):
	return pandas_loads((fp if hasattr(fp,'read') else Open(fp)).read(), sep=sep)


# encode pandas objects into strings
_convertible_set = {int, float, complex, bool, str, bytes, type(None)}
def pandas_encode(obj, sep=pandas_sep):
	if type(obj) in _convertible_set:
		return obj
	elif type(obj) == list:
		return [pandas_encode(i, sep=sep) for i in obj]
	elif type(obj) == tuple:
		return (pandas_encode(i, sep=sep) for i in obj)
	elif type(obj) == set:
		return {pandas_encode(i, sep=sep) for i in obj}
	elif type(obj) == dict:
		return {pandas_encode(k, sep=sep):pandas_encode(v, sep=sep) for k,v in obj.items()}
	elif type(obj) == pandas.DataFrame:
		return '\0'+str({'type':'DataFrame', 'csv':obj.to_csv(), 'index':list(obj.index.names)})
	elif type(obj) == pandas.Series:
		return '\0'+str({'type':'Series', 'csv':obj.to_csv()})
	elif type(obj) == types.ModuleType:
		return "\0<module %s>"%re.fullmatch("<module ([^ >]*)[^>]*>", str(obj)).group(1)
	return '\0'+str(obj)


# save object to string
def pandas_saves(obj, sep=pandas_sep):
	return repr(pandas_encode(obj))


# save object to file/filename
def pandas_save(obj, fp, sep=pandas_sep):
	(fp if hasattr(fp, 'write') else Open(fp, 'w')).write(pandas_saves(obj, sep=sep))


# for debugging only
if __name__ == '__main__':
	import pandas as pd
	import numpy as np
	df = pd.DataFrame(np.random.randint(0,256,[4,4]), columns=['index a1', 'index a2', 'b', 'c'],
					   index=pd.date_range('2020-01-01', '2020-01-04')).set_index(['index a1', 'index a2'], append=True)
	df0 = [1, 3.4, 1.1+2.1j, np.nan, None, True, False, b'ab12', 'abc', int, pd.DataFrame(), pd.DataFrame, type(pd.DataFrame), ['a', 1],
		   {'a':1, 'b':2, type:0, int:1, 0:df}, {1, 3.4, 1+2j, np.nan, True, None, int, 'aa', os, sys, pd.concat}]
	txt = pandas_saves(df0)
	df1 = pandas_loads(txt)

	assert True