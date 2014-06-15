wp-admin.py
===========
wp-admin.py is a Python module for managing WordPress installations from the
command line. Inspiration comes from both django-admin.py and
[WP-CLI](https://github.com/wp-cli/wp-cli).

Installing on Windows
---------------------
As long as you have Git Bash installed you just need to copy the wp-admin.py
module to C:\Python27\Scripts. Make sure that C:\Python27\ and
C:\Python27\Scripts are in your ```path``` environment variable.

Usage with Git Bash
-----
From the root of your WordPress project (directory containing wp-load.php):
```python
wp-admin.py starttheme [--classic] my-theme-name
```
The ```starttheme``` command will create the following directory structure
within the wp-contents/themes/ directory:
```
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
```
The above structure assumes you will be using the Twig template engine via
the [Timber](https://github.com/jarednova/timber) plugin. The ```starttheme```
command with the ```classic``` option will create the following directory
structure within the wp-contents/themes/ directory:
```
- my-theme-name
    - css/
    - images/
    - js/
    - 404.php
    - functions.php
    - index.php
    - README.md
    - style.css
```

To create a plugin skeleton:
```python
wp-admin.py startplugin my-plugin-name
```
The ```startplugin``` command will create the following directory structure
within the wp-contents/plugins/ directory:
```
- my-plugin-name
    - my-plugin.name.php
    - README.md
```
