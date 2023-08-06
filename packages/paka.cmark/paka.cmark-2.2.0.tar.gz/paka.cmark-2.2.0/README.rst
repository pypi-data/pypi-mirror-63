paka.cmark
==========
.. image:: https://travis-ci.org/PavloKapyshin/paka.cmark.svg?branch=master
    :target: https://travis-ci.org/PavloKapyshin/paka.cmark

``paka.cmark`` is a Python library that wraps subset of cmark_ C library
(that is one of reference implementations of CommonMark).


Features
--------
- Python 2.7 and 3.6 are supported
- PyPy (Python 2.7) is supported, as wrapping is made with CFFI_
- no need to install ``libcmark``, it is bundled with ``paka.cmark``
  (and sources of the former are regularly updated according to upstream)
- supported output: HTML, XML, CommonMark, man, LaTeX
- supported options: ``CMARK_OPT_UNSAFE``, ``CMARK_OPT_NOBREAKS``,
  ``CMARK_OPT_HARDBREAKS``, ``CMARK_OPT_SOURCEPOS``, ``CMARK_OPT_SMART``
- unlike ``libcmark``—underlying C library—``paka.cmark`` uses
  ``CMARK_OPT_NOBREAKS`` by default (``breaks`` argument allows to control
  line break rendering)
- safe HTML output is on by default (like in ``libcmark``)


Examples
--------
.. code-block:: pycon

    >>> from paka import cmark

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"<p>nope</p>"))
    <!-- raw HTML omitted -->

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS | CMARK_OPT_UNSAFE``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!", safe=False))
    <p>Hello, <em>World</em>!</p>


Render with ``CMARK_OPT_DEFAULT``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!", breaks=True))
    <p>Hello,
    <em>World</em>!</p>

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_HARDBREAKS``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!", breaks="hard"))
    <p>Hello,<br />
    <em>World</em>!</p>

Render CommonMark with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS``:

.. code-block:: pycon

    >>> print(cmark.to_commonmark(u"_Hello_"))
    *Hello*


Installation
------------
Library is `available on PyPI <https://pypi.org/project/paka.cmark/>`_,
you can use ``pip`` for installation:

.. code-block:: console

    $ pip install paka.cmark


Getting documentation
---------------------
Build HTML docs:

.. code-block:: console

    $ tox -e docs

View built docs:

.. code-block:: console

    $ sensible-browser .tox/docs/tmp/docs_html/index.html


Running tests
-------------
.. code-block:: console

    $ tox


Getting coverage
----------------
Collect info:

.. code-block:: console

    $ tox -e coverage

View HTML report:

.. code-block:: console

    $ sensible-browser .tox/coverage/tmp/cov_html/index.html


Checking code style
-------------------
Run code checkers:

.. code-block:: console

    $ tox -e checks


.. _cmark: https://github.com/commonmark/cmark
.. _CFFI: https://pypi.org/project/cffi/
