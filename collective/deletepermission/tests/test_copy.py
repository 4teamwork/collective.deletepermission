from AccessControl import Unauthorized
from collective.deletepermission.tests.base import FunctionalTestCase
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME


class TestCopy(FunctionalTestCase):

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
