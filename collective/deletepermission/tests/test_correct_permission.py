from collective.deletepermission.testing import COLLECTIVE_DELETEPERMISSION_INTEGRATION_TESTING
from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
from AccessControl import Unauthorized


class TestCorrectPermissions(TestCase):

    layer = COLLECTIVE_DELETEPERMISSION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        regtool = getToolByName(self.portal, 'portal_registration')

        #add members
        regtool.addMember('usera', 'usera',
                          properties={'username': 'usera',
                                      'fullname': 'f\xc3\xbcllnamea',
                                      'email': 'usera@email.com'})

        regtool.addMember('userb', 'userb',
                          properties={'username': 'userb',
                                      'fullname': 'f\xc3\xbcllnameb',
                                      'email': 'userb@email.com'})
        #create structure
        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'rootfolder'))
        self.folder.manage_addLocalRoles('usera', ['Contributor'])
        self.folder.manage_addLocalRoles('userb', ['Contributor'])
        logout()

        login(self.portal, 'usera')
        #create a folder and a document as usera
        self.folder_a = self.folder.get(
            self.folder.invokeFactory('Folder', 'folder-a'))
        self.doc_a = self.folder_a.get(
            self.folder_a.invokeFactory('Document', 'doc-a'))
        logout()

        #create a doc as userb
        login(self.portal, 'userb')
        self.doc_b = self.folder_a.get(
            self.folder_a.invokeFactory('Document', 'doc-b'))
        logout()

    def test_usera_remove_folder(self):
        """Test if usera can remove his folder"""
        login(self.portal, 'usera')
        self.folder.manage_delObjects('folder-a')

    def test_userb_remove_folder(self):
        """Test if userb can't delete usera's folder"""
        login(self.portal, 'userb')
        self.assertRaises(Unauthorized,
                          self.folder.manage_delObjects,
                          'folder-a')

    def test_usera_remove_doc_a(self):
        """Test if usera can remove his doc"""
        login(self.portal, 'usera')
        self.folder_a.manage_delObjects('doc-a')

    def test_usera_remove_doc_b(self):
        """Test if usera can remove userb's folder"""
        login(self.portal, 'usera')
        self.folder_a.manage_delObjects('doc-b')

    def test_userb_remove_doc_a(self):
        """Test if userb can remove usera's folder"""
        login(self.portal, 'userb')
        self.assertRaises(Unauthorized,
                          self.folder_a.manage_delObjects,
                          'doc-a')

    def test_userb_remove_doc_b(self):
        """Test if userb can remove his doc"""
        login(self.portal, 'userb')
        self.folder_a.manage_delObjects('doc-b')

    def test_remove_multiple(self):
        """Test if we still are able to remove multiple objects at once."""
        login(self.portal, 'usera')
        self.folder_a.manage_delObjects(['doc-a', 'doc-b'])
        self.assertEqual(self.folder_a.objectIds(), [])

    def test_remove_empty(self):
        """Check that we don't throw errors if we get a id that is none'"""
        login(self.portal, 'usera')
        self.folder_a.manage_delObjects(None)
