from AccessControl import Unauthorized
from collective.deletepermission.tests.base import duplicate_with_dexterity
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing


@duplicate_with_dexterity
class TestOnlyFiles(FunctionalTestCase):

    def setUp(self):
        self.user_a = create(Builder('user').with_userid('usera'))

        self.folder = create(self.folder_builder().titled(u'rootfolder'))
        self.set_local_roles(self.folder, self.user_a, 'Contributor')

        self.subfolder = create(self.folder_builder().titled(u'subfolder')
                                .within(self.folder))

        with self.user(self.user_a):
            self.firstleveldoc = create(self.folder_builder()
                                        .titled(u'doc-firstleveldoc')
                                        .within(self.folder))
            self.secondleveldoc = create(self.folder_builder()
                                         .titled(u'doc-secondleveldoc')
                                         .within(self.subfolder))

    @browsing
    def test_delete_secondlevel(self, browser):
        """Test if we are able to delete the file in the subfolder"""
        browser.login(self.user_a).open(self.secondleveldoc, view='delete_confirmation')
        browser.find('Delete').click()

    @browsing
    def test_delete_firstlevel(self, browser):
        """Test if we are able to delete the file in the rootfolder"""
        browser.login(self.user_a).open(self.firstleveldoc, view='delete_confirmation')
        browser.find('Delete').click()

    @browsing
    def test_delete_subfolder(self, browser):
        """Test if we can delete the subfolder. This should not be the case."""
        browser.login(self.user_a).open(self.subfolder, view='delete_confirmation')
        with self.assertRaises(Unauthorized):
            browser.find('Delete').click()
