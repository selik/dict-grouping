#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Rough implementation for the proposed ``dict.grouping``.
'''

from itertools import groupby


def grouping(iterable, key=None):
	'''
	Group elements of an iterable into a dict of lists.

	The ``key`` is a function computing a key value for each element.
	Each key corresponds to a list of elements in the same order as
	encountered. By default, the key will be the element itself.
	'''
	# https://en.wikipedia.org/wiki/Equivalence_class
	
	if key is None:
		return {k: list(g) for k, g in groupby(sorted(iterable))}

	groups = {}
	for x in iterable:
	    groups.setdefault(key(x), []).append(x)
	return groups


if __name__ == '__main__':
	import doctest
	doctest.testmod()
