===========
wpadmin
===========

.. image:: https://travis-ci.org/raulchacon/wpadmin.py.svg?branch=master
    :target: https://travis-ci.org/raulchacon/wpadmin.py

.. image:: https://coveralls.io/repos/raulchacon/wpadmin.py/badge.svg?branch=master
    :target: https://coveralls.io/r/raulchacon/wpadmin.py

A single Python module to assist with developing WordPress themes and plugins.
Inspiration comes from Django's ``startapp`` command.


Installation
---------------------

::

  $ pip install wpadmin


Usage
-------------------
From the root of your WordPress project (directory containing wp-load.php):

::

  $ wpadmin starttheme [--classic] my-theme-name


The ``starttheme`` command will create the following directory structure
within the wp-contents/themes/ directory:

::

  - my-theme-name
    - templates/
      - base.twig
    - static/
      - css/
      - images/
      - js/
    - 404.php
    - functions.php
    - index.php
    - README.md
    - style.css


The above structure assumes you will be using the Twig template engine via
the `Timber  <https://github.com/jarednova/timber>`_
plugin. The ``starttheme`` command with the ``--classic`` option
will create the following directory structure within the wp-contents/themes/
directory:

::

  - my-theme-name
    - css/
    - images/
    - js/
    - 404.php
    - functions.php
    - index.php
    - README.md
    - style.css


To create a plugin skeleton:

::

  $ wpadmin startplugin my-plugin-name


The ``startplugin`` command will create the following directory structure
within the wp-contents/plugins/ directory:

::

  - my-plugin-name
    - my-plugin.name.php
    - README.md


Running Tests
-------------------
::

  $ python -m unittest tests
