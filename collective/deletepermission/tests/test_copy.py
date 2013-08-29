from AccessControl import Unauthorized
from Products.statusmessages.interfaces import IStatusMessage
from collective.deletepermission import testing
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestCopy(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        login(self.portal, TEST_USER_NAME)

    def test_copy_works_without_beeing_able_to_delete(self):
        folder = create(Builder('folder'))
        self.revoke_permission('Delete portal content', on=folder)
        folder.object_copy()
        self.assertEquals([u'folder copied.'], self.get_status_messages())

    def test_copy_denied_without_copy_or_move_permission(self):
        folder = create(Builder('folder'))
        self.revoke_permission('Copy or Move', on=folder)
        with self.assertRaises(Unauthorized):
            folder.object_copy()

    def revoke_permission(self, permission, on):
        on.manage_permission(permission, roles=[], acquire=False)

    def get_status_messages(self):
        request = self.layer['request']
        messages = [msg.message for msg in IStatusMessage(request).show()]
        return messages
