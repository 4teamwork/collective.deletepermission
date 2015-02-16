from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from collective.deletepermission import testing
from contextlib import contextmanager
from ftw.builder import Builder
from ftw.testbrowser import browser
from plone.app.testing import login
from Products.statusmessages.interfaces import IStatusMessage
from unittest2 import TestCase
import sys
import transaction


class FunctionalTestCase(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING
    folder_name = 'Folder'

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

    def folder_builder(self):
        return Builder('folder')

    def is_dexterity_test(self):
        return False


def duplicate_with_dexterity(klass):
    """Decorator for duplicating a test suite to be ran against dexterity contents.
    """
    class DexterityTestSuite(klass):
        folder_name = 'dxfolder'

        def folder_builder(self):
            return Builder('dxfolder')

        def is_dexterity_test(self):
            return True

    DexterityTestSuite.__name__ = klass.__name__ + 'Dexterity'
    DexterityTestSuite.__module__ = klass.__module__
    sys._getframe(1).f_locals[DexterityTestSuite.__name__] = DexterityTestSuite
    return klass
