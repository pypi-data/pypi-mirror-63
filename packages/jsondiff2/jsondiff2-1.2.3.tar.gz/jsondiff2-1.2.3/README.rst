jsondiff
========

Diff JSON and JSON-like structures in Python.

Installation
------------

``pip install jsondiff``

Quickstart
----------

.. code-block:: python

    >>> from jsondiff import diff

    >>> diff({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
    {'c': 4, 'b': 3, delete: ['a']}

    >>> diff(['a', 'b', 'c'], ['a', 'b', 'c', 'd'])
    {insert: [(3, 'd')]}

    >>> diff(['a', 'b', 'c'], ['a', 'c'])
    {delete: [1]}

    # Typical diff looks like what you'd expect...
    >>> diff({'a': [0, {'b': 4}, 1]}, {'a': [0, {'b': 5}, 1]})
    {'a': {1: {'b': 5}}}

    # ...but similarity is taken into account
    >>> diff({'a': [0, {'b': 4}, 1]}, {'a': [0, {'c': 5}, 1]})
    {'a': {insert: [(1, {'c': 5})], delete: [1]}}

    # Support for various diff syntaxes
    >>> diff({'a': 1, 'b': 2}, {'b': 3, 'c': 4}, syntax='explicit')
    {insert: {'c': 4}, update: {'b': 3}, delete: ['a']}

    >>> diff({'a': 1, 'b': 2}, {'b': 3, 'c': 4}, syntax='symmetric')
    {insert: {'c': 4}, 'b': [2, 3], delete: {'a': 1}}

    # Special handling of sets
    >>> diff({'a', 'b', 'c'}, {'a', 'c', 'd'})
    {discard: set(['b']), add: set(['d'])}

    # Load and dump JSON
    >>> print diff('["a", "b", "c"]', '["a", "c", "d"]', load=True, dump=True)
    {"$delete": [1], "$insert": [[2, "d"]]}


Command Line Client
-------------------

Usage::

    jsondiff [-h] [-p] [-s SYNTAX] [-i INDENT] first second

    positional arguments:
      first
      second

    optional arguments:
      -h, --help            show this help message and exit
      -p, --patch
      -s SYNTAX, --syntax SYNTAX
      -i INDENT, --indent INDENT

Examples:

.. code-block:: bash

    $ jsondiff a.json b.json -i 2

    $ jsondiff a.json b.json -i 2 -s symmetric