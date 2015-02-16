from collective.deletepermission.tests.base import duplicate_with_dexterity
from AccessControl import Unauthorized
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import folder_contents
from ftw.testbrowser.pages import plone
from ftw.testbrowser.pages import statusmessages


@duplicate_with_dexterity
class TestCorrectPermissions(FunctionalTestCase):

    def setUp(self):
        self.user_a = create(Builder('user').with_userid('usera'))
        self.user_b = create(Builder('user').with_userid('userb'))

        self.folder = create(self.folder_builder().titled(u'rootfolder'))
        self.set_local_roles(self.folder, self.user_a, 'Contributor')
        self.set_local_roles(self.folder, self.user_b, 'Contributor')

        with self.user(self.user_a):
            self.folder_a = create(self.folder_builder().within(self.folder)
                                   .titled(u'folder-a'))
            self.doc_a = create(self.folder_builder().within(self.folder_a)
                                .titled(u'doc-a'))

        with self.user(self.user_b):
            self.doc_b = create(self.folder_builder().within(self.folder_a)
                                .titled(u'doc-b'))

    @browsing
    def test_userb_delete_docb(self, browser):
        """
        Check if User B is able to delete his own document.
        """
        browser.login(self.user_b).open(self.doc_b, view='delete_confirmation')
        browser.find('Delete').click()

    @browsing
    def test_userb_cut_docb(self, browser):
        """
        Check if User B is able to cut his own document.
        """
        browser.login(self.user_b).open(self.doc_b)
        browser.find('Cut').click()

    @browsing
    def test_userb_rename_docb(self, browser):
        """
        Check if User B is able to rename his own document.
        """
        browser.login(self.user_b).open(self.doc_b)
        browser.find('Rename').click()
        browser.fill({'new_ids:list': 'doc-b-renamed'}
                     ).find('Rename All').click()
        statusmessages.assert_no_error_messages()
        self.assertEquals(self.folder_a.absolute_url() + '/doc-b-renamed',
                          browser.url)

    @browsing
    def test_usera_remove_folder(self, browser):
        """
        Test if User A is able to delete his folder
        """
        browser.login(self.user_a).open(self.folder_a,
                                        view='delete_confirmation')
        browser.find('Delete').click()

    @browsing
    def test_usera_cut_folder(self, browser):
        """
        Test if User A is able to cut his folder
        """
        browser.login(self.user_a).open(self.folder_a)
        browser.find('Cut').click()

    @browsing
    def test_usera_rename_folder(self, browser):
        """
        Test if User A is able to rename his folder
        """
        browser.login(self.user_a).open(self.folder_a)
        browser.find('Rename').click()
        browser.fill({'new_ids:list': 'folder-a-renamed'}
                     ).find('Rename All').click()
        statusmessages.assert_no_error_messages()
        self.assertEquals(self.folder.absolute_url() + '/folder-a-renamed',
                          browser.url)

    @browsing
    def test_userb_remove_folder(self, browser):
        """
        Check if User B can delete User A's folder. Should not be possible.
        """
        browser.login(self.user_b).open(self.folder_a,
                                        view='delete_confirmation')
        with self.assertRaises(Unauthorized):
            browser.find("Delete").click()

    @browsing
    def test_userb_cut_folder(self, browser):
        """
        Check if User B can't cut User A's folder.
        """
        browser.login(self.user_b).open(self.folder_a)
        self.assertNotIn('Cut', self.get_actions())
        browser.open(self.folder_a, view='object_cut')
        self.assertEquals(['folder-a is not moveable.'],
                          statusmessages.error_messages())

    @browsing
    def test_userb_rename_folder(self, browser):
        """
        Check if User B can't rename User A's folder.
        """
        browser.login(self.user_b).open(self.folder_a)
        self.assertNotIn('Rename', self.get_actions())
        with self.assertRaises(Unauthorized):
            browser.open(self.folder_a, view='object_rename')

    @browsing
    def test_usera_remove_doc_a(self, browser):
        """
        Test if User A is able to delete his own Document.
        """
        browser.login(self.user_a).open(self.doc_a, view='delete_confirmation')
        browser.find("Delete").click()

    @browsing
    def test_usera_cut_doc_a(self, browser):
        """
        Test if User A is able to cut his own Document.
        """
        browser.login(self.user_a).open(self.doc_a)
        browser.find('Cut').click()

    @browsing
    def test_usera_rename_doc_a(self, browser):
        """
        Test if User A is able to rename his own Document.
        """
        browser.login(self.user_a).open(self.doc_a)
        browser.find('Rename').click()
        browser.fill({'new_ids:list': 'doc-a-renamed',
                      }).find('Rename All').click()
        statusmessages.assert_no_error_messages()
        self.assertEquals(self.folder_a.absolute_url() + '/doc-a-renamed',
                          browser.url)

    @browsing
    def test_usera_remove_doc_b(self, browser):
        """
        Test if User A is able to delete the Document of User B
        """
        browser.login(self.user_a).open(self.doc_b, view='delete_confirmation')
        browser.find('Delete').click()

    @browsing
    def test_usera_cut_doc_b(self, browser):
        """
        Test if User A is able to cut the Document of User B
        """
        browser.login(self.user_a).open(self.doc_b)
        browser.find('Cut').click()

    @browsing
    def test_usera_rename_doc_b(self, browser):
        """
        Test if User A is able to rename the Document of User B
        """
        browser.login(self.user_a).open(self.doc_b)
        browser.find('Rename').click()
        browser.fill({'new_ids:list': 'doc-b-renamed',
                      }).find('Rename All').click()
        statusmessages.assert_no_error_messages()
        self.assertEquals(self.folder_a.absolute_url() + '/doc-b-renamed',
                          browser.url)

    @browsing
    def test_userb_remove_doc_a(self, browser):
        """
        Check if User B can remove User A's Document. Should not be possible.
        """
        browser.login(self.user_b).open(self.doc_a, view='delete_confirmation')
        with self.assertRaises(Unauthorized):
            browser.find('Delete').click()

    @browsing
    def test_userb_cut_doc_a(self, browser):
        """
        Check if User B can't remove User A's Document.
        """
        browser.login(self.user_b).open(self.doc_a)
        self.assertNotIn('Cut', self.get_actions())
        browser.open(self.doc_a, view='object_cut')
        self.assertEquals(['doc-a is not moveable.'],
                          statusmessages.error_messages())

    @browsing
    def test_userb_rename_doc_a(self, browser):
        """
        Check if User B can't rename User A's Document.
        """
        browser.login(self.user_b).open(self.doc_a)
        self.assertNotIn('Rename', self.get_actions())
        with self.assertRaises(Unauthorized):
            browser.open(self.folder_a, view='object_rename')

    @browsing
    def test_usera_remove_docs_folder_contents(self, browser):
        """Check if we are able to remove files over folder_contents."""
        browser.login(self.user_a).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Delete').click()
        self.assertEqual(['Item(s) deleted.'], statusmessages.info_messages())

    @browsing
    def test_usera_cuts_docs_folder_contents(self, browser):
        """Check if we are able to cut docs over folder_contents."""
        browser.login(self.user_a).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Cut').click()
        self.assertEqual({'info': ['2 item(s) cut.'],
                          'warning': [],
                          'error': []}, statusmessages.messages())

    @browsing
    def test_usera_renames_docs_folder_contents(self, browser):
        """Check if we are able to rename docs over folder_contents."""
        browser.login(self.user_a).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Rename').click()
        self.assertEqual('folder_rename_form', plone.view())
        self.assertEqual('doc-a', browser.css('#doc-a_id').first.value)
        self.assertEqual('doc-b', browser.css('#doc-b_id').first.value)

    @browsing
    def test_userb_remove_docs_folder_contents(self, browser):
        """Check if the permission also works when we delete over
        folder_contents.
        """
        browser.login(self.user_b).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Delete').click()
        self.assertEqual(
            {'info': ['/plone/rootfolder/folder-a/doc-a'
                      ' could not be deleted.'],
             'warning': [],
             'error': []}, statusmessages.messages())

    @browsing
    def test_userb_cuts_docs_folder_contents(self, browser):
        """Check if the permission also works when we cut over
        folder_contents.
        """
        browser.login(self.user_b).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Cut').click()
        self.assertEqual({'info': [],
                          'warning': [],
                          'error': ['One or more items not moveable.']},
                         statusmessages.messages())

    @browsing
    def test_userb_renames_docs_folder_contents(self, browser):
        """Check if the permission also works when we rename over
        folder_contents.
        """
        browser.login(self.user_b).open(self.folder_a, view='folder_contents')
        folder_contents.select(self.doc_a, self.doc_b)
        folder_contents.form().find('Rename').click()
        self.assertEqual('folder_rename_form', plone.view())
        self.assertEqual(
            ['You are not allowed to modify the id of this item.',
             'You are not allowed to modify the title of this item.'],
            browser.css('#content fieldset .error span').text)
        self.assertFalse(browser.css('#doc-a_id'))
        self.assertEqual('doc-b', browser.css('#doc-b_id').first.value)
