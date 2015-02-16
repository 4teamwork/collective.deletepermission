from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
import plone.dexterity.content


class IDXFolder(Interface):
    title = schema.TextLine(
        title=u'Title',
        required=False)

alsoProvides(IDXFolder, IFormFieldProvider)


class DXFolder(plone.dexterity.content.Container):
    implements(IDXFolder)
