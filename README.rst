===========
wpadmin
===========

wpadmin is a Python module for managing WordPress installations from the
command line. Inspiration comes from both django-admin.py and `WP-CLI`_.

.. _WP-CLI: https://github.com/wp-cli/wp-cli


Installing
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
