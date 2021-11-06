from __future__ import print_function
from __future__ import division
from . import _C

import pandas as pd
import numpy as np

###################################################################################################################################################

def get_bar_latex(new_model_attrs, results_columns,
	uses_separator=False,
	):
	assert len(new_model_attrs)>0
	assert len(results_columns)>0
	separator = '|' if uses_separator else ''
	txt = 'c'*len(new_model_attrs)+separator+'c'*len(results_columns)
	txt = 'l'+txt[1:]
	return txt

def dict_to_dataframe(info_dict):
	return pd.DataFrame.from_dict(info_dict, orient='index'),

def get_slash():
	return '\\'

def get_dslash():
	return get_slash()*2

def get_cmidrule(a, b):
	return get_slash()+'cmidrule{'+str(a)+'-'+str(b)+'}'

def get_hline(
	n=None,
	):
	if n is None:
		return get_slash()+'hline'
	else:
		return get_slash()+'hlineB{'+str(n)+'}'

def get_rule(a, b):
	return get_slash()+'rule{0pt}{'+str(a)+'ex}'+get_slash()+'rule[-'+str(b)+'ex]{0pt}{0ex}'

def get_bold(s:str):
	return get_slash()+'textbf{'+s+'}'