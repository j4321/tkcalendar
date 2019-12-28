from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='tkcalendar',
      version='1.6.1',
      description='Calendar and DateEntry widgets for Tkinter',
      long_description=long_description,
      url='https://github.com/j4321/tkcalendar',
      author='Juliette Monsel',
      author_email='j_4321@protonmail.com',
      license='GPLv3',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Widget Sets',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Operating System :: OS Independent'],
      keywords=['tkinter', 'calendar', 'date'],
      install_requires=["babel"],
      py_modules=["tkcalendar.calendar_",
                  "tkcalendar.dateentry",
                  "tkcalendar.tooltip"],
      packages=["tkcalendar"])
