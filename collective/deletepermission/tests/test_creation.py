from collective.deletepermission.tests.base import duplicate_with_dexterity
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import plone
from ftw.testbrowser.pages import statusmessages
import transaction


@duplicate_with_dexterity
class TestFactoryPatch(FunctionalTestCase):

    @browsing
    def test_object_addable_without_delete_permission(self, browser):
        user = create(Builder('user').with_roles('Contributor'))
        self.revoke_permission('Delete portal content', on=self.layer['portal'])
        transaction.commit()

        browser.login(user).open()
        factoriesmenu.add(self.folder_name)
        browser.fill({'Title': 'Foo'}).save()
        statusmessages.assert_no_error_messages()
        self.assertEquals('folder_listing', plone.view())
