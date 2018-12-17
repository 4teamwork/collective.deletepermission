from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from collective.deletepermission import testing
from contextlib import contextmanager
from ftw.builder import Builder
from ftw.testbrowser.pages import editbar
from plone.app.testing import login
from unittest2 import TestCase
import sys
import transaction


class FunctionalTestCase(TestCase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING
    folder_name = 'Folder'

    def revoke_permission(self, permission, on):
        on.manage_permission(permission, roles=[], acquire=False)
        transaction.commit()

    def set_local_roles(self, context, user, *roles):
        if hasattr(user, 'getUserName'):
            user = user.getUserName()

        context.manage_setLocalRoles(user, tuple(roles))
        context.reindexObjectSecurity()
        transaction.commit()

    def get_actions(self):
        return editbar.menu_options("Actions")

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

    if testing.IS_PLONE_5_OR_GREATER:
         # The default types (Folder etc.) in Plone 5 are already Dexterity.
         # So we do not test Archetypes under Plone 5 anymore, thus we do not
         # need to duplicate the tests.
         return klass

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
