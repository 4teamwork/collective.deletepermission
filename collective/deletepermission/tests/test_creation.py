import transaction
from collective.deletepermission.testing import IS_PLONE_5_OR_GREATER
from collective.deletepermission.tests.base import (FunctionalTestCase,
                                                    duplicate_with_dexterity)
from ftw.builder import Builder, create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu, plone, statusmessages


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
        if IS_PLONE_5_OR_GREATER:
            self.assertEquals('listing_view', plone.view())
        else:
            self.assertEquals('folder_listing', plone.view())
