from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from collective.deletepermission import testing
from contextlib import contextmanager
from ftw.testbrowser import browser
from plone.app.testing import login
from Products.statusmessages.interfaces import IStatusMessage
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def revoke_permission(self, permission, on):
        on.manage_permission(permission, roles=[], acquire=False)

    def set_local_roles(self, context, user, *roles):
        if hasattr(user, 'getUserName'):
            user = user.getUserName()

        context.manage_setLocalRoles(user, tuple(roles))
        context.reindexObjectSecurity()
        transaction.commit()

    def get_status_messages(self):
        request = self.layer['request']
        messages = [msg.message for msg in IStatusMessage(request).show()]
        return messages

    def get_actions(self):
        return browser.css('#plone-contentmenu-actions .actionMenuContent a').text

    @contextmanager
    def user(self, username):
        if hasattr(username, 'getUserName'):
            username = username.getUserName()

        sm = getSecurityManager()
        login(self.layer['portal'], username)
        try:
            yield
        finally:
            setSecurityManager(sm)
