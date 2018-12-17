from collective.deletepermission.testing import IS_PLONE_5_OR_GREATER
from collective.deletepermission.tests.base import duplicate_with_dexterity
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import statusmessages
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


@duplicate_with_dexterity
class TestCopy(FunctionalTestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        login(self.portal, TEST_USER_NAME)

    @browsing
    def test_copy_works_without_being_able_to_delete(self, browser):
        folder = create(self.folder_builder())
        self.revoke_permission('Delete portal content', on=folder)
        browser.login().open(folder)
        self.assertFalse(api.user.has_permission("Delete portal content", obj=folder))
        self.assertTrue(api.user.has_permission("Copy or Move", obj=folder))
        browser.find("Copy").click()
        if IS_PLONE_5_OR_GREATER:
            self.assertEqual(['copied.'], statusmessages.info_messages())
        else:
            if self.is_dexterity_test():
                self.assertEquals([u'dxfolder copied.'], statusmessages.info_messages())
            else:
                self.assertEquals([u'folder copied.'], statusmessages.info_messages())

    @browsing
    def test_copy_denied_without_copy_or_move_permission(self, browser):
        folder = create(self.folder_builder())
        self.revoke_permission('Copy or Move', on=folder)
        browser.login().open(folder)
        self.assertFalse(api.user.has_permission("Copy or Move", obj=folder))

        # The "copy" action is not available, so we cannot click it at all.
        self.assertIsNone(browser.find("Copy"))

        # Advanced users may guess the url.
        with browser.expect_unauthorized():
            browser.open(folder, view="object_copy")
