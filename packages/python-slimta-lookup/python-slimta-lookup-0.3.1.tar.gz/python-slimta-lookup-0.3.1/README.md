#### [Project Homepage][1]

--------------------

About
=====

Provides a simple way to control [`slimta`][3] actions and policies with
external lookups. This extension is for convenience and does not provide any
new functionality. It was inspired by and is mostly compatible with [Dovecot's
password database][4] concept.

[![Build Status](https://travis-ci.org/slimta/python-slimta-lookup.svg?branch=master)](https://travis-ci.org/slimta/python-slimta-lookup)
[![Coverage Status](https://coveralls.io/repos/github/slimta/python-slimta-lookup/badge.svg?branch=master)](https://coveralls.io/github/slimta/python-slimta-lookup?branch=master)

Getting Started
===============

If you haven't yet installed [`python-slimta`][2], refer to the "Getting
Started" section. Once inside your virtualenv:

    (.venv)$ python setup.py develop

To run the suite of included unit tests:

    (.venv)$ py.test

[1]: http://slimta.org/
[2]: https://github.com/slimta/python-slimta
[3]: http://slimta.org/latest/manual/slimta.html
[4]: http://wiki2.dovecot.org/PasswordDatabase

