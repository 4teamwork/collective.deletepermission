from collective.deletepermission.testing import (
    COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING)
from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
from OFS.CopySupport import CopyError

import transaction


class TestCorrectPermissions(TestCase):

    layer = COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

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

        transaction.commit()

        # | obj            | user a             | user b             |
        # | folder-a       | Contributor, Owner | Contributor        |
        # | folder-a/doc-a | Contributor, Owner | Contributor        |
        # | folder-a/doc-b | Contributor        | Contributor, Owner |

    def test_usera_cut_folder(self):
        """usera should be able to cut his own folder
        becauase he is its Owner"""

        login(self.portal, 'usera')
        self.folder.manage_cutObjects(['folder-a'])

    def test_userb_cut_folder(self):
        """userb should NOT be able to cut usera's folder, because he is
        not its Owner"""

        login(self.portal, 'userb')
        self.assertRaises(CopyError,
                          self.folder.manage_cutObjects,
                          ['folder-a'])

    def test_usera_cut_doc_a(self):
        """usera should be able to cut doc-a, because he is its Owner"""

        login(self.portal, 'usera')
        self.folder_a.manage_cutObjects(['doc-a'])

    def test_usera_cut_doc_b(self):
        """usera should be able to cut doc-b, because ???????????????????"""
        # XXX why?

        login(self.portal, 'usera')
        self.folder_a.manage_cutObjects(['doc-b'])

    def test_userb_cut_doc_a(self):
        """userb should NOT be able to cut coc-a, because his not Owner"""
        # XXX should this be raised upon paste??

        login(self.portal, 'userb')
        self.assertRaises(CopyError,
                          self.folder_a.manage_cutObjects,
                          'doc-a')

    def test_userb_cut_doc_b(self):
        """userb should be able to cut his own document"""

        login(self.portal, 'userb')
        self.folder_a.manage_cutObjects(['doc-b'])

    def test_cut_multiple(self):
        """Cutting objects INCLUDING an object which cannot be cut should not
        raise, so that the OTHER object is cut (not the transaction not
        cancelled because of the exception)
        """

        login(self.portal, 'usera')
        self.folder_a.manage_cutObjects(['doc-a', 'doc-b'])

    def test_cut_empty(self):
        """Cutting "None" should throw a ValueError."""

        login(self.portal, 'usera')
        self.assertRaises(ValueError, self.folder_a.manage_cutObjects, None)
