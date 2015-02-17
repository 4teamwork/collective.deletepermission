from setuptools import setup, find_packages
import os

version = '1.2.0'

tests_require = [
    'AccessControl',
    'Products.CMFCore',
    'Products.GenericSetup',
    'Products.statusmessages',
    'Zope2',
    'ftw.builder',
    'ftw.testbrowser',
    'plone.app.dexterity',
    'plone.app.portlets',
    'plone.app.testing',
    'plone.autoform',
    'transaction',
    'unittest2',
    'zExceptions',
    'zope.interface',
    ]


extras_require = {
    'tests': tests_require,
    }


long_description = (
    open('README.rst').read()
    + '\n' +
    open(os.path.join('docs', 'HISTORY.txt')).read()
    + '\n')

setup(name='collective.deletepermission',
      version=version,
      description="Implements a new permission 'Delete portal content'",
      long_description=long_description.decode('utf-8'),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='collective deletepermission 4teamwork ftw plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/collective.deletepermission',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'AccessControl',
        'Acquisition',
        'Products.Archetypes',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'Products.PythonScripts',
        'ZODB3',
        'Zope2',
        'collective.monkeypatcher',
        'ftw.upgrade',
        'setuptools',
        'zope.container',
        'zope.event',
        'zope.lifecycleevent',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
