#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

    # На хостинге:
    #path = "/home/a/a223223/binary_com/public_html"
    # -------------------------------
    # append project.path to sys.path
    # -------------------------------
    #if not path in sys.path:
    #    sys.path.append(path)
    #sys.path.insert(0, '%s/env/lib/python3.4/site-packages' % path)

    xapian_path = os.path.dirname(os.path.abspath(__file__))
    xapian_site_packages = os.path.join(xapian_path, 'xapian64', 'site-packages')
    sys.path.insert(0, xapian_site_packages)
    xapian_libs = os.path.join(xapian_path, 'xapian64', 'lib')
    sys.path.insert(0, xapian_libs)

    #djapian = os.path.join(xapian_site_packages, 'djapian')
    #sys.path.insert(1, djapian)

    # -----------------
    # USAGE:
    # python3 manage.py
    # -----------------

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    print(os.readlink('conf/.env')) # runserver --noreload
    main()
