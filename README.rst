Pyap2: Python address parser
============================


Pyap2 is a maintained fork of Pyap, a regex-based python library for
detecting and parsing addresses. Currently it supports US 🇺🇸, Canadian 🇨🇦, British 🇬🇧 and Australian 🇦🇺 addresses. 


.. code-block:: python

    >>> import pyap
    >>> test_address = """
        Lorem ipsum
        225 E. John Carpenter Freeway, 
        Suite 1500 Irving, Texas 75062
        Dorem sit amet
        """
    >>> addresses = pyap.parse(test_address, country='US')
    >>> for address in addresses:
            # shows found address
            print(address)
            # shows address parts
            print(address.as_dict())
    ...




Installation
------------

To install Pyap2, simply:

.. code-block:: bash

    $ pip install pyap2



About
-----
We started improving the original `pyap` by adopting poetry and adding typing support. 
It was extensively tested in web-scraping operations on thousands of US addresses. 
Gradually, we added support for many rarer address formats and edge cases, as well 
as the ability to parse a partial address where only street info is available. 


Typical workflow
----------------
Pyap should be used as a first thing when you need to detect an address
inside a text when you don't know for sure whether the text contains
addresses or not.


Limitations
-----------
Because Pyap2 (and Pyap) is based on regular expressions it provides fast results.
This is also a limitation because regexps intentionally do not use too
much context to detect an address.

In other words in order to detect US address, the library doesn't
use any list of US cities or a list of typical street names. It
looks for a pattern which is most likely to be an address.

For example the string below would be detected as a valid address: 
"1 SPIRITUAL HEALER DR SHARIF NSAMBU SPECIALISING IN"

It happens because this string has all the components of a valid
address: street number "1", street name "SPIRITUAL HEALER" followed
by a street identifier "DR" (Drive), city "SHARIF NSAMBU SPECIALISING"
and a state name abbreviation "IN" (Indiana).

The good news is that the above mentioned errors are **quite rare**.


