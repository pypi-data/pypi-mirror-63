***PERSIST QUEUE PACKAGE*** 
===========================

This project is based on the achievements of `persist-queue <https://pypi.org/project/persist-queue/>`

``persistQueue`` is a class that created for ease the develop.

Requirements
--------------
* Python 2.7
* Full suport for Linux

Installation
--------------

```pip install persistQueue==__version__```

* Adding path for python shell

```echo export PYTHONPATH=.local/lib/python2.7/site-packages/persistQueue:${PYTHONPATH} >> .bashrc```

Examples
--------
Example usage with a SQLite3 based queue

.. code-block:: python

    >>> from persistQueue import PersistQueue
    >>> q = PersistQueue()
    >>> q.put('str1')
    >>> q.put('str2')
    >>> q.put('str3')
    >>> q.get()
    'str1'
    >>> del q

