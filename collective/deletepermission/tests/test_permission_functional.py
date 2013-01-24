from AccessControl import Unauthorized
from collective.deletepermission.testing import (
    COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING)
from mechanize._mechanize import LinkNotFoundError
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
import transaction


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

    def tearDown(self):
        super(TestCorrectPermissions, self).tearDown()
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        portal.manage_delObjects(['rootfolder'])
        transaction.commit()

    def _auth_a(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'usera', 'usera',))

    def _auth_b(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            'userb', 'userb',))

    def test_userb_delete_docb(self):
        """
        Check if User B is able to delete his own document.
        """
        self._auth_b()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_userb_cut_docb(self):
        """
        Check if User B is able to cut his own document.
        """
        self._auth_b()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b')
        link = self.browser.getLink("Cut")
        self.assertTrue(link)

        link.click()

    def test_userb_rename_docb(self):
        """
        Check if User B is able to rename his own document.
        """
        self._auth_b()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b')
        link = self.browser.getLink("Rename")
        self.assertTrue(link)

        link.click()

        self.browser.getControl(name="new_ids:list").value = 'doc-b-renamed'
        self.browser.getControl(name="form.button.RenameAll").click()

        self.assertEquals(self.browser.url,
            self.folder_a.absolute_url() + '/doc-b-renamed')

    def test_usera_remove_folder(self):
        """
        Test if User A is able to delete his folder
        """
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_usera_cut_folder(self):
        """
        Test if User A is able to cut his folder
        """
        self._auth_a()

        self.browser.open(self.folder_a.absolute_url())
        link = self.browser.getLink("Cut")

        self.assertTrue(link)
        link.click()

    def test_usera_rename_folder(self):
        """
        Test if User A is able to rename his folder
        """
        self._auth_a()

        self.browser.open(self.folder_a.absolute_url())
        link = self.browser.getLink("Rename")

        self.assertTrue(link)
        link.click()

        self.browser.getControl(name="new_ids:list").value = 'folder-a-renamed'
        self.browser.getControl(name="form.button.RenameAll").click()

        self.assertEquals(self.browser.url,
            self.folder.absolute_url() + '/folder-a-renamed')

    def test_userb_remove_folder(self):
        """
        Check if User B can delete User A's folder. Should not be possible.
        """
        self._auth_b()

        self.browser.open(
            self.folder_a.absolute_url() + '/delete_confirmation')
        self.assertRaises(Unauthorized,
                          self.browser.getControl("Delete").click)

    def test_userb_cut_folder(self):
        """
        Check if User B can't cut User A's folder.
        """
        self._auth_b()
        self.browser.open(self.folder_a.absolute_url())

        self.assertRaises(LinkNotFoundError, self.browser.getLink, 'Cut')

        self.assertRaises(Unauthorized,
                          self.folder_a.restrictedTraverse('object_cut'))

    def test_userb_rename_folder(self):
        """
        Check if User B can't rename User A's folder.
        """
        self._auth_b()
        self.browser.open(self.folder_a.absolute_url())

        self.assertRaises(LinkNotFoundError, self.browser.getLink, 'Rename')

        self.assertRaises(Unauthorized,
                          self.folder_a.restrictedTraverse('object_rename'))

    def test_usera_remove_doc_a(self):
        """
        Test if User A is able to delete his own Document.
        """
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-a/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_usera_cut_doc_a(self):
        """
        Test if User A is able to cut his own Document.
        """
        self._auth_a()

        self.browser.open(self.doc_a.absolute_url())
        link = self.browser.getLink('Cut')

        self.assertTrue(link)
        link.click()

    def test_usera_rename_doc_a(self):
        """
        Test if User A is able to rename his own Document.
        """
        self._auth_a()

        self.browser.open(self.doc_a.absolute_url())
        link = self.browser.getLink('Rename')

        self.assertTrue(link)
        link.click()

        self.browser.getControl(name="new_ids:list").value = 'doc-a-renamed'
        self.browser.getControl(name="form.button.RenameAll").click()

        self.assertEquals(self.browser.url,
            self.folder_a.absolute_url() + '/doc-a-renamed')

    def test_usera_remove_doc_b(self):
        """
        Test if User A is able to delete the Document of User B
        """
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-b/delete_confirmation')
        self.browser.getControl("Delete").click()

    def test_usera_cut_doc_b(self):
        """
        Test if User A is able to cut the Document of User B
        """
        self._auth_a()

        self.browser.open(self.doc_b.absolute_url())
        link = self.browser.getLink('Cut')

        self.assertTrue(link)
        link.click()

    def test_usera_rename_doc_b(self):
        """
        Test if User A is able to rename the Document of User B
        """
        self._auth_a()

        self.browser.open(self.doc_b.absolute_url())
        link = self.browser.getLink('Rename')

        self.assertTrue(link)
        link.click()

        self.browser.getControl(name="new_ids:list").value = 'doc-b-renamed'
        self.browser.getControl(name="form.button.RenameAll").click()

        self.assertEquals(self.browser.url,
            self.folder_a.absolute_url() + '/doc-b-renamed')

    def test_userb_remove_doc_a(self):
        """
        Check if User B can remove User A's Document. Should not be possible.
        """
        self._auth_b()

        self.browser.open(
            self.folder_a.absolute_url() + '/doc-a/delete_confirmation')
        self.assertRaises(Unauthorized,
                          self.browser.getControl("Delete").click)

    def test_userb_cut_doc_a(self):
        """
        Check if User B can't remove User A's Document.
        """
        self._auth_b()

        self.browser.open(self.doc_a.absolute_url())

        self.assertRaises(LinkNotFoundError, self.browser.getLink,
                         'Cut')

        self.assertRaises(Unauthorized,
                          self.folder_a.restrictedTraverse('object_cut'))

    def test_userb_rename_doc_a(self):
        """
        Check if User B can't rename User A's Document.
        """
        self._auth_b()

        self.browser.open(self.doc_a.absolute_url())

        self.assertRaises(LinkNotFoundError, self.browser.getLink,
                         'Rename')

        self.assertRaises(Unauthorized,
                          self.folder_a.restrictedTraverse('object_rename'))

    def test_usera_remove_docs_folder_contents(self):
        """Check if we are able to remove files over folder_contents."""
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_delete:method").click()
        self.assertIn('<dd>Item(s) deleted.</dd>', self.browser.contents)

    def test_usera_cuts_docs_folder_contents(self):
        """Check if we are able to cut docs over folder_contents."""
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_cut:method").click()
        self.assertNotIn('<dd>One or more items not moveable.</dd>',
                         self.browser.contents)

    def test_usera_renames_docs_folder_contents(self):
        """Check if we are able to rename docs over folder_contents."""
        self._auth_a()

        self.browser.open(
            self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_rename_form:method").click()

        self.assertEquals(self.browser.contents.count('paths:list'), 2)

    def test_userb_remove_docs_folder_contents(self):
        """Check if the permission also works when we delete over
        folder_contents.
        """
        self._auth_b()

        self.browser.open(self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_delete:method").click()
        self.assertIn('<dd>/plone/rootfolder/folder-a/doc-a could not be '
                      'deleted.</dd>',
                      self.browser.contents)

    def test_userb_cuts_docs_folder_contents(self):
        """Check if the permission also works when we cut over
        folder_contents.
        """
        self._auth_b()

        self.browser.open(self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_cut:method").click()
        self.assertIn('<dd>One or more items not moveable.</dd>',
                      self.browser.contents)

    def test_userb_renames_docs_folder_contents(self):
        """Check if the permission also works when we rename over
        folder_contents.
        """
        self._auth_b()

        self.browser.open(self.folder_a.absolute_url() + '/folder_contents')
        self.browser.getControl("doc-a").selected = True
        self.browser.getControl("doc-b").selected = True
        self.browser.getControl(name="folder_rename_form:method").click()

        self.assertEquals(self.browser.contents.count('paths:list'), 1)
