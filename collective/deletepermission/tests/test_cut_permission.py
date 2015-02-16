from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from OFS.CopySupport import CopyError


class TestCorrectPermissions(FunctionalTestCase):

    def setUp(self):
        self.user_a = create(Builder('user').with_userid('usera'))
        self.user_b = create(Builder('user').with_userid('userb'))

        self.folder = create(Builder('folder').titled('rootfolder'))
        self.set_local_roles(self.folder, self.user_a, 'Contributor')
        self.set_local_roles(self.folder, self.user_b, 'Contributor')

        with self.user(self.user_a):
            self.folder_a = create(Builder('folder').within(self.folder)
                                   .with_id('folder-a'))
            self.doc_a = create(Builder('document').within(self.folder_a)
                                .with_id('doc-a'))

        with self.user(self.user_b):
            self.doc_b = create(Builder('document').within(self.folder_a)
                                .with_id('doc-b'))

    def test_usera_cut_folder(self):
        """usera should be able to cut his own folder
        becauase he is its Owner"""

        with self.user(self.user_a):
            self.folder.manage_cutObjects(['folder-a'])

    def test_userb_cut_folder(self):
        """userb should NOT be able to cut usera's folder, because he is
        not its Owner"""

        with self.user(self.user_b):
            self.assertRaises(CopyError,
                              self.folder.manage_cutObjects,
                              ['folder-a'])

    def test_usera_cut_doc_a(self):
        """usera should be able to cut doc-a, because he is its Owner"""

        with self.user(self.user_a):
            self.folder_a.manage_cutObjects(['doc-a'])

    def test_usera_cut_doc_b(self):
        """usera should be able to cut doc-b, because ???????????????????"""
        # XXX why?

        with self.user(self.user_a):
            self.folder_a.manage_cutObjects(['doc-b'])

    def test_userb_cut_doc_a(self):
        """userb should NOT be able to cut coc-a, because his not Owner"""
        # XXX should this be raised upon paste??

        with self.user(self.user_b):
            self.assertRaises(CopyError,
                              self.folder_a.manage_cutObjects,
                              'doc-a')

    def test_userb_cut_doc_b(self):
        """userb should be able to cut his own document"""

        with self.user(self.user_b):
            self.folder_a.manage_cutObjects(['doc-b'])

    def test_cut_multiple(self):
        """Cutting objects INCLUDING an object which cannot be cut should not
        raise, so that the OTHER object is cut (not the transaction not
        cancelled because of the exception)
        """

        with self.user(self.user_a):
            self.folder_a.manage_cutObjects(['doc-a', 'doc-b'])

    def test_cut_empty(self):
        """Cutting "None" should throw a ValueError."""

        with self.user(self.user_a):
            self.assertRaises(ValueError, self.folder_a.manage_cutObjects, None)
