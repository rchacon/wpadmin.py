# -*- coding: utf-8 -*-
import os
import sys
import unittest
from testfixtures import TempDirectory

import wpadmin


class PseudoArgs(object):
    def __init__(self, name, project_root, classic=None):
        self.name = name
        self.project_root = project_root
        self.classic = classic


class WpAdminApiTests(unittest.TestCase):
    def setUp(self):
        self.wp_dir = TempDirectory()
        self.not_wp_dir = TempDirectory()

        # Turn wp_dir into fake WordPress root directory
        self.theme_roots = os.path.join(
            self.wp_dir.path,
            'wp-content',
            'themes'
        )
        
        os.makedirs(self.theme_roots)

        self.plugin_root = os.path.join(
            self.wp_dir.path,
            'wp-content',
            'plugins'
        )
        
        os.makedirs(self.plugin_root)

    def tearDown(self):
        self.wp_dir.cleanup()
        self.not_wp_dir.cleanup()

    def test_starttheme_from_project_root(self):
        """Creates the following directory structure within
        the themes directory:
        - mytheme
            - templates/
                - base.twig
            - static/
                - css/
                - images/
                - js/
            - 404.php
            - functions.php
            - index.php
            - style.css
            - README.md
            - .gitignore
        """
        args = PseudoArgs(name='mytheme', project_root=self.wp_dir.path)

        wpadmin.starttheme(args)

        mytheme = os.path.join(self.theme_roots, 'mytheme')

        path_to_base_twig = os.path.join(mytheme, 'templates', 'base.twig')

        self.assertTrue(os.path.isfile(path_to_base_twig))

        for d in ['css', 'images', 'js']:
            path_to_dir = os.path.join(mytheme, 'static', d)
            self.assertTrue(os.path.isdir(path_to_dir))

        theme_files = [
            '404.php',
            'functions.php',
            'index.php',
            'style.css',
            'README.md',
            '.gitignore'
        ]

        for f in theme_files:
            self.assertTrue(os.path.isfile(os.path.join(mytheme, f)))

    def test_starttheme_from_project_root_with_classic_option(self):
        """Creates the following directory structure within
        the themes directory:

        - mytheme
            - css/
            - images/
            - js/
            - 404.php
            - functions.php
            - index.php
            - style.css
            - README.md
            - .gitignore
        """
        context = {
            'name': 'mytheme',
            'classic': True,
            'project_root': self.wp_dir.path
        }

        args = PseudoArgs(**context)

        wpadmin.starttheme(args)

        mytheme = os.path.join(self.theme_roots, 'mytheme')

        for d in ['css', 'images', 'js']:
            self.assertTrue(os.path.isdir(os.path.join(mytheme, d)))

        theme_files = [
            '404.php',
            'functions.php',
            'index.php',
            'style.css',
            'README.md',
            '.gitignore'
        ]

        for f in theme_files:
            self.assertTrue(os.path.isfile(os.path.join(mytheme, f)))

    def test_starttheme_from_outside_project_root(self):
        """Raises NotInWordPressRootError
        """
        args = PseudoArgs(name='mytheme', project_root=self.not_wp_dir.path)

        self.assertRaises(
            wpadmin.NotInWordPressRootError,
            wpadmin.starttheme,
            args
        )

    def test_starttheme_from_outside_project_root_with_classic_option(self):
        """Raises NotInWordPressRootError
        """
        context = {
            'name': 'mytheme',
            'classic': True,
            'project_root': self.not_wp_dir.path
        }

        args = PseudoArgs(**context)

        self.assertRaises(
            wpadmin.NotInWordPressRootError,
            wpadmin.starttheme,
            args
        )

    def test_startplugin_from_project_root(self):
        """Create the following directory structure within the themes
        directory

        - myplugin
            - myplugin.php
            - README.md
            - .gitignore
        """
        args = PseudoArgs(name='myplugin', project_root=self.wp_dir.path)

        wpadmin.startplugin(args)

        myplugin = os.path.join(self.plugin_root, 'myplugin')

        for f in ['myplugin.php', 'README.md', '.gitignore']:
            self.assertTrue(os.path.isfile(os.path.join(myplugin, f)))

    def test_startplugin_from_outside_project_root(self):
        """Raises NotInWordPressRootError
        """
        args = PseudoArgs(name='myplugin', project_root=self.not_wp_dir.path)

        self.assertRaises(
            wpadmin.NotInWordPressRootError,
            wpadmin.startplugin,
            args
        )


class PseudoFile(list):
    """Simplified file interface."""
    write = list.append

    def getvalue(self):
        return ''.join(self)


class WpAdminShellTests(unittest.TestCase):
    """Test the usual CLI options"""

    def setUp(self):
        self._saved_argv = sys.argv
        self._saved_stdout = sys.stdout
        self._saved_stderr = sys.stderr
        self._config_filenames = []
        self.stdin = ''
        sys.argv = ['wpadmin']
        sys.stdout = PseudoFile()
        sys.stderr = PseudoFile()

    def tearDown(self):
        sys.argv = self._saved_argv
        sys.stdout = self._saved_stdout
        sys.stderr = self._saved_stderr

    def wpadmin(self, *args):
        del sys.stdout[:], sys.stderr[:]
        sys.argv[1:] = args
        try:
            wpadmin._main()
            errorcode = None
        except SystemExit:
            errorcode = sys.exc_info()[1].code
        return sys.stdout.getvalue(), sys.stderr.getvalue(), errorcode

    def test_print_usage(self):
        stdout, stderr, errcode = self.wpadmin('--help')
        self.assertFalse(errcode)
        self.assertFalse(stderr)
        self.assertTrue(stdout.startswith("usage: wpadmin [-h] {starttheme,"))

    def test_starttheme(self):
        stdout, stderr, errcode = self.wpadmin('starttheme')
        self.assertEqual(2, errcode)
        self.assertTrue("too few arguments" in stderr)

    def test_starttheme_with_classic_shorthand_option(self):
        stdout, stderr, errcode = self.wpadmin('starttheme -c')
        self.assertEqual(2, errcode)
        self.assertTrue(stderr.startswith("usage: wpadmin [-h] {starttheme,"))

    def test_starttheme_with_classic_option(self):
        stdout, stderr, errcode = self.wpadmin('starttheme --classic')
        self.assertEqual(2, errcode)
        self.assertTrue(stderr.startswith("usage: wpadmin [-h] {starttheme,"))

    def test_startplugin(self):
        stdout, stderr, errcode = self.wpadmin('startplugin')
        self.assertEqual(2, errcode)
        self.assertTrue("too few arguments" in stderr)


if __name__ == "__main__":
    unittest.main()
