from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import Interface, alsoProvides


class IDXFolder(Interface):
    pass

alsoProvides(IDXFolder, IFormFieldProvider)
