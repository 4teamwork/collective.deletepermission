from collective.deletepermission import testing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from unittest2 import TestCase
import transaction


class TestFactoryPatch(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def test_object_addable_without_delete_permission(self):
        portal = self.layer['portal']
        self.revoke_permission('Delete portal content', on=portal)
        self.grant_roles('Contributor')
        transaction.commit()

        self.visit(portal.absolute_url() +
                   '/createObject?type_name=Folder')
        self.fill('Title', 'Foo')
        self.save()
        self.assert_url('http://nohost/plone/foo')

    def revoke_permission(self, permission, on):
        on.manage_permission(permission, roles=[], acquire=False)

    def grant_roles(self, *roles):
        setRoles(self.layer['portal'], TEST_USER_ID, roles)

    def visit(self, url):
        self.browser = Browser(self.layer['app'])
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.handleErrors = False
        self.browser.open(url)

    def fill(self, label, value):
        self.browser.getControl(label=label).value = value

    def save(self):
        self.browser.getControl(label='Save').click()

    def assert_url(self, url, msg=None):
        self.assertEquals(url.rstrip('/'), self.browser.url.rstrip('/'), msg)
