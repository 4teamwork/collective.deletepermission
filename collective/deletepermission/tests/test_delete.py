from collective.deletepermission import testing
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from unittest2 import TestCase
from zExceptions import Unauthorized


class TestDeleeting(TestCase):
    layer = testing.COLLECTIVE_DELETEPERMISSION_INTEGRATION_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])
        login(self.layer['portal'], TEST_USER_NAME)

    def test_delete_possible_with_both_permissions(self):
        parent = create(Builder('folder'))
        child = create(Builder('folder').within(parent))

        parent.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)
        child.manage_permission('Delete portal content',
                                roles=['Contributor'], acquire=False)

        self.assertIn(child.getId(), parent.objectIds())
        parent.manage_delObjects([child.getId()])
        self.assertNotIn(child.getId(), parent.objectIds())

    def test_delete_unauthorized_when_no_permission_on_child(self):
        parent = create(Builder('folder'))
        child = create(Builder('folder').within(parent))

        parent.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)
        child.manage_permission('Delete portal content',
                                roles=[], acquire=False)

        with self.assertRaises(Unauthorized):
            parent.manage_delObjects([child.getId()])

    def test_delete_unauthorized_when_no_permission_on_parent(self):
        parent = create(Builder('folder'))
        child = create(Builder('folder').within(parent))

        from AccessControl import getSecurityManager
        sm = getSecurityManager()
        self.assertEqual(1, sm.checkPermission('Delete objects', parent))

        parent.manage_permission('Delete objects',
                                 roles=[], acquire=False)
        child.manage_permission('Delete portal content',
                                roles=['Contributor'], acquire=False)

        self.assertEqual(None, sm.checkPermission('Delete objects', parent))

        with self.assertRaises(Unauthorized):
            parent.manage_delObjects([child.getId()])
