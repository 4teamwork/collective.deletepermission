from setuptools import setup, find_packages
import os

version = '1.1.3'
maintainer = "Timon Tschanz"

tests_require = [
    'AccessControl',
    'Products.CMFCore',
    'Products.GenericSetup',
    'Zope2',
    'lxml',
    'mechanize',
    'plone.app.portlets',
    'plone.app.testing',
    'plone.testing',
    'transaction',
    'unittest2',
    'zope.configuration',
    'ftw.builder',
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
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/collective.deletepermission',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'AccessControl',
          'Products.Archetypes',
          'Products.CMFCore',
          'Products.CMFPlone',
          'Products.PythonScripts',
          'collective.monkeypatcher',
          'ftw.upgrade',
          'setuptools',
          # -*- Extra requirements: -*-
      ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
