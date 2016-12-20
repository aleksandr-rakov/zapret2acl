import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'waitress',
    'pyquery',
    'pyramid_mako',
    'ipaddr',
    'suds'
    ]

setup(name='zapret2acl',
      version='0.0',
      description='zapret2acl',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="zapret2acl",
      entry_points="""\
      [paste.app_factory]
      main = zapret2acl:main
      [console_scripts]
       zapret2acl = zapret2acl.console:main
      """,
      )
