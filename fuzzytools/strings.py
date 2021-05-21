from __future__ import print_function
from __future__ import division
from . import C_

import os
from termcolor import colored
import numpy as np
import random

###################################################################################################################################################

def delete_string_chars(s, chars):
	return ''.join([c for c in s if not c in chars])

def random_repeat_string(s, a, b):
	r = random.randint(a, b)
	return s*r

def random_augment_string(s, a, b):
	l = [random_repeat_string(c, a, b) for c in s]
	return ''.join(l)

def get_dict_from_string(string:str,
	key_key_separator:str=C_.KEY_KEY_SEP_CHAR,
	key_value_separator:str=C_.KEY_VALUE_SEP_CHAR,
	):
	pairs = string.split(key_key_separator)
	ret = {}
	for p in pairs:
		split = p.split(key_value_separator)
		if len(split)==2:
			key, value = split
			ret[key] = value
	return ret

def get_string_from_dict(d:str,
	key_key_separator:str=C_.KEY_KEY_SEP_CHAR,
	key_value_separator:str=C_.KEY_VALUE_SEP_CHAR,
	keep_none_values=False,
	):
	ret = key_key_separator.join([f'{key}{key_value_separator}{d[key]}' for key in d.keys() if keep_none_values or not d[key] is None])
	return ret

def get_bar(
	char:str=C_.MIDDLE_LINE_CHAR,
	N:int=C_.BAR_SIZE,
	):
	if N is None:
		try:
			N = os.get_terminal_size().columns
		except OSError:
			N = C_.JUPYTER_NOTEBOOK_BAR_SIZE
	return char*N

def string_replacement(string:str, replace_dict:dict):
	'''
	Reeplace multiple sub-strings in a string.
	Example:
	string: Hi to all the hidden demons.
	replace_dict: {'hi':'Hellow', 'demons': 'dogs', ' ':'_'}
	Return: Hellow_to_all_the_hidden_dogs.

	Parameters
	----------
	string (str): the target string
	replace_dict (dict): This is a dictionary where the keys are the target sub-string to be replaced and the values are the sub-string replacement.
					The replacement are in the key order.

	Return
	----------
	new_string (str): the new string
	'''
	assert isinstance(replace_dict, dict)
	new_string = string
	for key in replace_dict:
		new_string = new_string.replace(key,replace_dict[key])

	return new_string

def query_strings_in_string(query_strings:list, string:str,
	mode:str='or',
	):
	'''
	Search if at least one query_string is in a string
	'''
	assert isinstance(query_strings, list)
	assert isinstance(string, str)
	values = [int(i in string) for i in query_strings]
	if mode=='or':
		return sum(values)>0
	elif mode=='and':
		return sum(values)==len(values)
	else:
		raise Exception(f'no mode {mode}')

def color_str(txt, color):
	if color is None or txt=='':
		return txt
	else:
		return colored(txt, color)

###################################################################################################################################################

def _format_float(x,
	n_decimals:int=C_.N_DECIMALS,
	remove_zero=C_.REMOVE_ZERO,
	):
	if np.isnan(x):
		return C_.NAN_CHAR
	txt = format(x, f',.{n_decimals}f')
	if remove_zero and abs(x)<1:
		txt = txt.replace('0.', '.')
	return txt

def _format_int(x):
	if np.isnan(x):
		return C_.NAN_CHAR
	return f'{x:,}'

def xstr(x,
	n_decimals:int=C_.N_DECIMALS,
	remove_zero=C_.REMOVE_ZERO,
	add_pos=False,
	):
	p = '+' if add_pos and x>0 else ''
	if x is None:
		return C_.NAN_CHAR
	if isinstance(x, str):
		return x
	if isinstance(x, int):
		return p+_format_int(x) # int
	if isinstance(x, float):
		return p+_format_float(x, n_decimals, remove_zero) # float

	### numpy
	if isinstance(x, np.ndarray):
		t = str(x.dtype)
		if 'int' in t:
			return p+_format_int(x) # int
		if 'float' in t:
			return p+_format_float(x, n_decimals, remove_zero) # float

	raise Exception(f'wrong xstr {type(x)}')