from __future__ import print_function
from __future__ import division
from . import C_

from itertools import cycle
from copy import copy, deepcopy
import random
import numpy as np

###################################################################################################################################################

class BalancedCyclicBoostraping():
	def __init__(self, l_objs, l_classes,
		n=None,
		uses_shuffle=True,
		uses_counter=False,
		):
		assert len(l_objs)==len(l_classes)
		self.l_objs = l_objs
		self.l_classes = l_classes
		self.n = n
		self.uses_shuffle = uses_shuffle
		self.uses_counter = uses_counter
		self.reset()

	def __len__(self):
		return len(self.l_objs)

	def reset(self):
		self.reset_counter()
		self.class_names, counts = np.unique(self.l_classes, return_counts=True)
		self.n = max(counts) if self.n is None else self.n
		self.l_objs_dict = {}
		for c in self.class_names:
			self.l_objs_dict[c] = [obj for obj,_c in zip(self.l_objs, self.l_classes) if _c==c]
		self.reset_cycles()
	
	def reset_counter(self):
		self.counter = {obj:0 for obj in self.l_objs}

	def reset_cycles(self):
		if self.uses_shuffle:
			self.shuffle()
		self.cycles_dict = {c:cycle(self.l_objs_dict[c]) for c in self.class_names}
	
	def shuffle(self):
		for c in self.class_names:
			random.shuffle(self.l_objs_dict[c])
			
	def size(self):
		return self.n*len(self.class_names)
	
	def get_samples(self):
		samples = []
		for c in self.class_names:
			samples += [next(self.cycles_dict[c]) for _ in range(0, self.n)]
		if self.uses_counter:
			for s in samples:
				self.counter[s] += 1
		return samples
	
	def __call__(self):
		return self.get_samples()