from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from zope.interface import Interface


class IDXFolder(Interface):
    pass

alsoProvides(IDXFolder, IFormFieldProvider)
