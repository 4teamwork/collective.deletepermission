from collective.deletepermission.testing import (
    COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING)
from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone.app.testing import logout
import transaction
from plone.testing.z2 import Browser
from AccessControl import Unauthorized


class TestCorrectPermissions(TestCase):

    layer = COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        #add members
        regtool = getToolByName(self.portal, 'portal_registration')

        regtool.addMember('usera', 'usera',
                          properties={'username': 'usera',
                                      'fullname': 'f\xc3\xbcllnamea',
                                      'email': 'usera@email.com'})

        regtool.addMember('userb', 'userb',
                          properties={'username': 'userb',
                                      'fullname': 'f\xc3\xbcllnameb',
                                      'email': 'userb@email.com'})
        #create folders
        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'rootfolder'))
        self.folder.manage_addLocalRoles('usera', ['Contributor'])
        self.folder.manage_addLocalRoles('userb', ['Contributor'])
        logout()

        #change user and create objects. We need to do this so the owner is
        # set right.
        login(self.portal, 'usera')
        self.folder_a = self.folder.get(
            self.folder.invokeFactory('Folder', 'folder-a'))
        self.doc_a = self.folder_a.get(
            self.folder_a.invokeFactory('Document', 'doc-a'))
        logout()

        login(self.portal, 'userb')
        self.doc_b = self.folder_a.get(
            self.folder_a.invokeFactory('Document', 'doc-b'))
        logout()
        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def test_userb_delete_docb(self):
        """
        Check if User B is able to delete his own document.
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'userb', 'userb',))

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_usera_remove_folder(self):
        """
        Test if User A is able to delete his folder
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.folder_a.absolute_url() + '/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_userb_remove_folder(self):
        """
        Check if User B can delete User A's folder. Should not be possible.
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'userb', 'userb',))

        self.browser.open(
            self.folder_a.absolute_url() + '/delete_confirmation')
        self.assertRaises(Unauthorized,
                          self.browser.getControl("Delete").click)

    def test_usera_remove_doc_a(self):
        """
        Test if User A is able to delete his own Document.
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-a/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_usera_remove_doc_b(self):
        """
        Test if User A is able to delete the Document of User B
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_userb_remove_doc_a(self):
        """
        Check if User B can remove User A's Document. Should not be possible.
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'userb', 'userb',))

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-a/delete_confirmation')
        self.assertRaises(Unauthorized,
                          self.browser.getControl("Delete").click)

    def test_usera_remove_docs_folder_contents(self):
        """Check if we are able to remove files over folder_contents."""
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

        self.browser.open(
            self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_delete:method").click()
        self.assertIn('<dd>Item(s) deleted.</dd>', self.browser.contents)

    def test_userb_remove_docs_folder_contents(self):
        """Check if the permission also works when we delete over
        folder_contents.
        """
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'userb', 'userb',))

        self.browser.open(self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_delete:method").click()
        self.assertIn('<dd>/plone/rootfolder/folder-a/doc-a could not be '
                      'deleted.</dd>',
                      self.browser.contents)
