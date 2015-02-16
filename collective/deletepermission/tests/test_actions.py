from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
import transaction


class TestDeleteAction(FunctionalTestCase):

    def setUp(self):
        self.hugo = create(Builder('user').named('Hugo', 'Boss')
                           .with_roles('Member', 'Contributor'))
        self.john = create(Builder('user').named('John', 'Doe')
                           .with_roles('Member', 'Contributor'))
        with self.user(self.hugo):
            self.container = create(Builder('folder'))
        with self.user(self.john):
            self.content = create(Builder('folder').within(self.container))

    @browsing
    def test_user_can_delete_own_contents(self, browser):
        browser.login(self.john).visit(self.content)
        self.assertIn('Delete', self.get_actions(),
                      'A user should be able to delete his own content.')

    @browsing
    def test_user_can_not_delete_without_delete_objects_on_parent(self,
                                                                  browser):
        self.revoke_permission('Delete objects', on=self.container)
        transaction.commit()
        browser.login(self.john).visit(self.content)
        self.assertNotIn('Delete', self.get_actions(),
                         'A user should not be able to delete content'
                         ' without "Delete objects" on the parent.')


class TestCutAction(FunctionalTestCase):

    def setUp(self):
        self.hugo = create(Builder('user').named('Hugo', 'Boss')
                           .with_roles('Member', 'Contributor'))
        self.john = create(Builder('user').named('John', 'Doe')
                           .with_roles('Member', 'Contributor'))
        with self.user(self.hugo):
            self.container = create(Builder('folder'))
        with self.user(self.john):
            self.content = create(Builder('folder').within(self.container))

    @browsing
    def test_user_can_cut_own_contents(self, browser):
        browser.login(self.john).visit(self.content)
        self.assertIn('Cut', self.get_actions(),
                      'A user should be able to cut his own content.')

    @browsing
    def test_user_can_not_cut_without_delete_objects_on_parent(self, browser):
        self.revoke_permission('Delete objects', on=self.container)
        transaction.commit()
        browser.login(self.john).visit(self.content)
        self.assertNotIn('Cut', self.get_actions(),
                         'A user should not be able to cut content'
                         ' without "Delete objects" on the parent.')
