#!/c/Python27/python
# wpadmin.py - Command line tool for WordPress
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Raul Chacon <raulchacon@outlook.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

r"""
For usage and a list of options, try this:
$ python wpadmin.py -h

This program lives here:
https://github.com/raulchacon/wpadmin.py
"""
__version__ = '0.1.1'

import os
from functools import wraps


class NotInWordPressRootError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def wp_root(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (os.path.isdir(os.path.join(args[0].project_root, 'wp-content',
            'themes')) and
            os.path.isdir(os.path.join(args[0].project_root, 'wp-content',
                          'plugins'))):
            return f(*args, **kwargs)

        raise NotInWordPressRootError('You must run this script from \
                                      the WordPress root folder.')
    return decorated_function


@wp_root
def starttheme(args):
    """Creates theme folder with the following empty files/folders:
    index.php, style.css, images/, css/ and js/. If with_timber is
    True then it additionally creates views/base.twig
    """
    # Create Theme folder
    theme_root = os.path.join(args.project_root, 'wp-content', 'themes',
                              args.name)
    os.makedirs(theme_root)

    # Create files
    theme_files = [
        '404.php',
        'functions.php',
        'index.php',
        'style.css',
        'README.md',
        '.gitignore'
    ]

    for f in theme_files:
        fh = open(os.path.join(theme_root, f), 'w')
        if '.php' in f:
            fh.write("<?php\n\n")
        fh.close()

    if args.classic:
        static_dir = theme_root
    else:
        # Create a static sub directory
        static_dir = os.path.join(theme_root, 'static')
        os.makedirs(static_dir)

        # Change default twig directory from "views" to "templates"
        functionsphp = open(os.path.join(theme_root, 'functions.php'), 'a')
        functionsphp.write("Timber::$dirname = 'templates';\n")
        functionsphp.close()
        twig_templates = os.path.join(theme_root, 'templates')
        os.makedirs(os.path.join(twig_templates))
        open(os.path.join(twig_templates, 'base.twig'), 'a').close()

    # Create sub directories
    for d in ['images', 'css', 'js']:
        os.makedirs(os.path.join(static_dir, d))


@wp_root
def startplugin(args):
    """Creates plugin folder with a php file of the same name."""
    plugin_root = os.path.join(
        args.project_root,
        'wp-content',
        'plugins',
        args.name
    )

    os.makedirs(plugin_root)

    open(os.path.join(plugin_root, 'README.md'), 'a').close()
    open(os.path.join(plugin_root, '.gitignore'), 'a').close()

    with open(os.path.join(plugin_root, args.name + '.php'), 'w') as f:
        f.write("<?php\n\n")


def _main():
    """Parse options and execute wpadmin commands"""
    import argparse

    # Create top level parser
    parser = argparse.ArgumentParser(description="Create WordPress \
                                     theme/plugin skeleton")
    subparsers = parser.add_subparsers()

    # Create the parser for the "starttheme" command
    parser_starttheme = subparsers.add_parser('starttheme')
    parser_starttheme.add_argument('name')
    parser_starttheme.add_argument("-c", "--classic", help="create classic theme \
                                    skeleton", action="store_true")
    parser_starttheme.set_defaults(project_root=os.getcwd())
    parser_starttheme.set_defaults(func=starttheme)

    # Create the parser for the "startplugin" command
    parser_startplugin = subparsers.add_parser('startplugin')
    parser_startplugin.add_argument('name')
    parser_startplugin.set_defaults(project_root=os.getcwd())
    parser_startplugin.set_defaults(func=startplugin)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":

    _main()
