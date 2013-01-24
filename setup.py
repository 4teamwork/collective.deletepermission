from setuptools import setup, find_packages
import os

version = '1.0'
maintainer = "Timon Tschanz"

tests_require = [
    'unittest2',
    'plone.app.testing',
    'plone.testing',
    'transaction',
    'zope.configuration',
    'AccessControl',
    'Products.CMFCore',
    'Products.GenericSetup',
    'plone.app.portlets',
    'Zope2',
    'mechanize',
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
          'setuptools',
          'AccessControl',
          'Products.CMFCore',
          'Products.CMFPlone',
          'Products.PythonScripts',
          'Products.Archetypes',
          'collective.monkeypatcher',
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
