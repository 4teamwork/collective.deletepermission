from AccessControl import getSecurityManager
from collective.deletepermission.tests.base import duplicate_with_dexterity
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from zExceptions import Unauthorized


@duplicate_with_dexterity
class TestDeleeting(FunctionalTestCase):

    def setUp(self):
        self.contributor = create(Builder('user').with_roles('Contributor'))
        self.parent = create(self.folder_builder())
        self.child = create(self.folder_builder().within(self.parent))

    def test_delete_possible_with_both_permissions(self):
        self.parent.manage_permission('Delete objects',
                                 roles=['Contributor'], acquire=False)
        self.child.manage_permission('Delete portal content',
                                roles=['Contributor'], acquire=False)

        with self.user(self.contributor):
            self.assertIn(self.child.getId(), self.parent.objectIds())
            self.parent.manage_delObjects([self.child.getId()])
            self.assertNotIn(self.child.getId(), self.parent.objectIds())

    def test_delete_unauthorized_when_no_permission_on_child(self):
        self.parent.manage_permission('Delete objects',
                                      roles=['Contributor'], acquire=False)
        self.child.manage_permission('Delete portal content',
                                     roles=[], acquire=False)

        with self.user(self.contributor):
            with self.assertRaises(Unauthorized):
                self.parent.manage_delObjects([self.child.getId()])

    def test_delete_unauthorized_when_no_permission_on_parent(self):
        with self.user(self.contributor):
            checkPermission = getSecurityManager().checkPermission
            self.assertTrue(checkPermission('Delete objects', self.parent))

            self.parent.manage_permission('Delete objects',
                                          roles=[], acquire=False)
            self.child.manage_permission('Delete portal content',
                                         roles=['Contributor'], acquire=False)

            self.assertFalse(checkPermission('Delete objects', self.parent))
            with self.assertRaises(Unauthorized):
                self.parent.manage_delObjects([self.child.getId()])
