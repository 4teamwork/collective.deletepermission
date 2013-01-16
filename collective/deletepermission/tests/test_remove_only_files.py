from collective.deletepermission.testing import COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING
from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
from AccessControl import Unauthorized
import transaction
from plone.testing.z2 import Browser


class TestOnlyFiles(TestCase):

    layer = COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        #add members
        regtool = getToolByName(self.portal, 'portal_registration')

        regtool.addMember('usera', 'usera',
                          properties={'username': 'usera',
                                      'fullname': 'f\xc3\xbcllnamea',
                                      'email': 'usera@email.com'})

        # create structure
        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'rootfolder'))
        self.folder.manage_addLocalRoles('usera', ['Contributor'])
        self.subfolder = self.folder.get(
            self.folder.invokeFactory('Folder', 'subfolder'))
        logout()

        # Login as user and create some docs. We need to change user so the
        # owner is set right
        login(self.portal, 'usera')
        self.firstleveldoc = self.folder.get(
            self.folder.invokeFactory('Document', 'doc-firstlevel'))
        self.secondleveldoc = self.subfolder.get(
            self.subfolder.invokeFactory('Document', 'doc-secondlevel'))
        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def test_delete_secondlevel(self):
        """Test if we are able to delete the file in the subfolder"""
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.portal.absolute_url() + '/rootfolder/subfolder/doc-secondleve'
                                         'l/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_delete_firstlevel(self):
        """Test if we are able to delete the file in the rootfolder"""
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.portal.absolute_url() + '/rootfolder/doc-firstlevel/delete_'
                                         'confirmation')
        self.browser.getControl("Delete").click()

    def test_delete_subfolder(self):
        """Test if we can delete the subfolder. This should not be the case."""
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.portal.absolute_url() + '/rootfolder/subfolder/delete_'
                                         'confirmation')
        self.assertRaises(Unauthorized,
                          self.browser.getControl("Delete").click)
