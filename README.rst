########################################################################
PEP ???? -- dict.grouping
########################################################################

We currently have three reasonable techniques to create groups from a
sequence or iterable:

- itertools.groupby
- collections.defaultdict
- dict.setdefault

Unfortunately, both ``itertools.groupby`` and
``collections.defaultdict`` are error-prone, and ``dict.setdefault`` is
homely (not beautiful).


The ``defaultdict`` is elegant for building a grouping, but many
otherwise-expert programmers will accidentally insert new groups when
they intended to raise a ``KeyError``.

Elegant for creating groups:

	>>> from collections import defaultdict
	>>> groups = defaultdict(set)
	>>> for x in range(7):
	...     groups[x % 2].add(x)
	...

Error-prone when using groups:

	>>> groups
	defaultdict(<class 'set'>, {0: {0, 2, 4, 6}, 1: {1, 3, 5}})
	>>> len(groups[2]) 	# accidentally inserts a new group
	0
	>>> groups
	defaultdict(<class 'set'>, {0: {0, 2, 4, 6}, 1: {1, 3, 5}, 2: set()})
	

Many users of ``itertools.groupby`` will forget to sort
the data before grouping, accidentally creating two or more separate
groups for the same key.

	>>> from itertools import groupby
	>>> mod_2 = lambda x: x % 2

Mistake:

	>>> {k: set(group) for k, group in groupby(range(7), key=mod_2)}
	{0: {6}, 1: {5}}

Correct:
	
	>>> numbers = sorted(range(7), key=mod_2)
	>>> {k: set(group) for k, group in groupby(numbers, key=mod_2)}
	{0: {0, 2, 4, 6}, 1: {1, 3, 5}}


The ``dict.setdefault`` method is often the best choice for grouping,
but suffers from a less-beautiful appearance. Secondarily,
``setdefault`` cannot easily create a grouping as an expression.

	>>> groups = {}
	>>> for x in range(7):
	...     groups.setdefault(x % 2, set()).add(x)
	...
	>>> groups
	{0: {0, 2, 4, 6}, 1: {1, 3, 5}}


========================================================================
Proposal
========================================================================

I propose a new ``dict`` classmethod, ``dict.grouping`` which will
construct a new dictionary based on an iterable and a key-function.

	>>> # grouping = dict.grouping


	>>> mod_2 = lambda x: x % 2
	>>> grouping(range(7), mod_2)
	{0: [0, 2, 4, 6], 1: [1, 3, 5]}


	>>> grouping('ababa')
	{'a': ['a', 'a', 'a'], 'b': ['b', 'b']}


	>>> grouping('aBAb', str.casefold)
	{'a': ['a', 'A'], 'b': ['B', 'b']}


	>>> grouping('aBAbaB', str.casefold)
	{'a': ['a', 'A', 'a'], 'b': ['B', 'b', 'B']}


While ``dict.grouping`` creates a dict of lists, preserving the order
that group members were encountered, it is often useful to create
"equivalence classes" which are better modeled as a dictionary of sets.

	>>> groups = grouping('aBAbaB', str.casefold)
	>>> {k: sorted(set(g)) for k, g in groups.items()}
	{'a': ['A', 'a'], 'b': ['B', 'b']}


If each group should be a multiset, where repetitions matter but order
does not, then a dictionary of Counters is appropriate.

	>>> from collections import Counter
	>>> groups = grouping('aBAbaB', str.casefold)
	>>> {k: Counter(g) for k, g in groups.items()}
	{'a': Counter({'a': 2, 'A': 1}), 'b': Counter({'B': 2, 'b': 1})}
