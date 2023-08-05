:tocdepth: 2

sleek-lvalert Documentation
===========================

sleek-lvalert is a client for the LIGO/Virgo LVAlert pubsub infrastructure that
is powered by :doc:`slixmpp <slixmpp:index>`. It requires Python 3.5 or later.

Quick Start
-----------

Install with pip_::

    pip install sleek-lvalert

Put your username and password in your netrc_ file in ``~/.netrc``::

    echo 'machine lvalert-test.cgca.uwm.edu login albert.einstein password gravity' >> ~/.netrc
    chmod 0600 ~/.netrc

Subscribe to some nodes::

    lvalert subscribe cbc_gstlal cbc_pycbc cbc_mbtaonline

Listen for LVAlert messages::

    lvalert listen

Command Line Interface
----------------------

.. argparse::
    :module: sleek_lvalert.tool
    :func: parser

API Reference
-------------

.. autoclass:: sleek_lvalert.LVAlertClient

    :members:

    .. autosummary::

        get_nodes
        get_subscriptions
        listen
        start
        stop
        subscribe
        unsubscribe


.. _netrc: https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html
.. _pip: http://pip.pypa.io
