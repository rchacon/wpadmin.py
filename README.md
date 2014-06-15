wp-admin.py
===========
wp-admin.py is a Python module for managing WordPress installations from the
command line.

Installing on Windows
---------------------
As long as you have Git Bash installed you just need to copy the module to
C:\Python27\Scripts.

Usage
-----
From the root of your WordPress project (directory containing wp-load.php):
```python
wp-admin.py starttheme [--timber] my-theme-name
```
The ```starttheme``` command will create the following directory structure within
the wp-contents/themes/ directory:
```
- my-theme-name
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
If you include the timber option the following directory and file will
additionally be created within "my-theme-name":
```
- templates/
    - base.twig
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
