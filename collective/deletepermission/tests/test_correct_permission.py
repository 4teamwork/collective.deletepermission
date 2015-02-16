from AccessControl import Unauthorized
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create


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

    def test_usera_remove_folder(self):
        """Test if usera can remove his folder"""
        with self.user(self.user_a):
            self.folder.manage_delObjects('folder-a')

    def test_userb_remove_folder(self):
        """Test if userb can't delete usera's folder"""
        with self.user(self.user_b):
            self.assertRaises(Unauthorized,
                              self.folder.manage_delObjects,
                              'folder-a')

    def test_usera_remove_doc_a(self):
        """Test if usera can remove his doc"""
        with self.user(self.user_a):
            self.folder_a.manage_delObjects('doc-a')

    def test_usera_remove_doc_b(self):
        """Test if usera can remove userb's folder"""
        with self.user(self.user_a):
            self.folder_a.manage_delObjects('doc-b')

    def test_userb_remove_doc_a(self):
        """Test if userb can remove usera's folder"""
        with self.user(self.user_b):
            self.assertRaises(Unauthorized,
                              self.folder_a.manage_delObjects,
                              'doc-a')

    def test_userb_remove_doc_b(self):
        """Test if userb can remove his doc"""
        with self.user(self.user_b):
            self.folder_a.manage_delObjects('doc-b')

    def test_remove_multiple(self):
        """Test if we still are able to remove multiple objects at once."""
        with self.user(self.user_a):
            self.folder_a.manage_delObjects(['doc-a', 'doc-b'])
            self.assertEqual(self.folder_a.objectIds(), [])

    def test_remove_empty(self):
        """Check that we don't throw errors if we get a id that is none'"""
        with self.user(self.user_a):
            self.folder_a.manage_delObjects(None)
