#!/c/Python27/python
"""
Command line tool for WordPress
"""
import os
import argparse
from functools import wraps


class NotInWordPressRootError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WPCommand(object):
    def wp_root(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if (os.path.isdir(os.path.join(os.getcwd(), 'wp-content',
                'themes')) and
                os.path.isdir(os.path.join(os.getcwd(), 'wp-content',
                              'plugins'))):
                return f(*args, **kwargs)

            raise NotInWordPressRootError('You must run this script from \
                                          the WordPress root folder.')
        return decorated_function

    @staticmethod
    @wp_root
    def createtheme(args):
        """Creates theme folder with the following empty files/folders:
        index.php, style.css, images/, css/ and js/. If with_timber is
        True then it additionally creates views/base.twig
        """
        theme_root = os.path.join(os.getcwd(), 'wp-content', 'themes',
                                  args.name)
        os.makedirs(theme_root)

        for f in ['index.php', 'README.md', 'style.css', 'functions.php',
                  '404.php']:
            fh = open(os.path.join(theme_root, f), 'w')
            if '.php' in f:
                fh.write("<?php\n\n")
            fh.close()

        static_dir = os.path.join(theme_root, 'static')
        os.makedirs(static_dir)

        for d in ['images', 'css', 'js']:
            os.makedirs(os.path.join(static_dir, d))

        # Create files for a Timber based theme
        if args.timber:
            functionsphp = open(os.path.join(theme_root, 'functions.php'), 'a')
            functionsphp.write("Timber::$dirname = 'templates';\n")
            functionsphp.close()

            twig_templates = os.path.join(theme_root, 'templates')
            os.makedirs(os.path.join(twig_templates))
            open(os.path.join(twig_templates, 'base.twig'), 'a').close()

    @staticmethod
    @wp_root
    def createplugin(args):
        """Creates plugin folder with a php file of the same name."""
        plugin_root = os.path.join(os.getcwd(), 'wp-content', 'plugins',
                                   args.name)
        os.makedirs(plugin_root)

        open(os.path.join(plugin_root, 'README.md'), 'a').close()
        f = open(os.path.join(plugin_root, args.name + '.php'), 'w')
        f.write("<?php\n\n")
        f.close()


if __name__ == "__main__":

    # Create top level parser
    parser = argparse.ArgumentParser(description="Create WordPress \
                                     theme/plugin skeleton")
    subparsers = parser.add_subparsers()

    # Create the parser for the "createtheme" command
    parser_createtheme = subparsers.add_parser('createtheme')
    parser_createtheme.add_argument('name')
    parser_createtheme.add_argument("-t", "--timber", help="create timber based theme \
                                    skeleton", action="store_true")
    parser_createtheme.set_defaults(func=WPCommand.createtheme)

    # Create the parser for the "createplugin" command
    parser_createplugin = subparsers.add_parser('createplugin')
    parser_createplugin.add_argument('name')
    parser_createplugin.set_defaults(func=WPCommand.createplugin)

    args = parser.parse_args()
    args.func(args)
