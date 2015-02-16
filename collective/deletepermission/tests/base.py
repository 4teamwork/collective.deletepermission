from collective.deletepermission import testing
from Products.statusmessages.interfaces import IStatusMessage
from unittest2 import TestCase


class FunctionalTestCase(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def revoke_permission(self, permission, on):
        on.manage_permission(permission, roles=[], acquire=False)

    def get_status_messages(self):
        request = self.layer['request']
        messages = [msg.message for msg in IStatusMessage(request).show()]
        return messages
