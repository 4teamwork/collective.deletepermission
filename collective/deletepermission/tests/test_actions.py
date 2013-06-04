from Products.CMFCore.utils import getToolByName
from collective.deletepermission import testing
from lxml.cssselect import CSSSelector
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.testing.z2 import Browser
from unittest2 import TestCase
from zope.container.interfaces import INameChooser
import lxml.html
import transaction


class ActionTestBase(TestCase):

    def create_user(self, with_id, identified_by='password', with_roles=None):
        if with_roles is None:
            with_roles = ['Member']

        acl_users = getToolByName(self.layer['portal'], 'acl_users')
        acl_users.userFolderAddUser(with_id, identified_by, with_roles, [])

    def given_object(self, titled, creator, within=None, of_type='Folder'):
        if within is None:
            within = self.layer['portal']

        login(self.layer['portal'], creator)

        chooser = INameChooser(within)
        newid = chooser.chooseName(titled, within)
        within.invokeFactory(of_type, newid, title=titled)
        obj = within.get(newid)
        obj.processForm()

        transaction.commit()

        logout()
        return obj

    def open_browser(self, visit, as_user=SITE_OWNER_NAME,
                     identifed_by='password'):

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                as_user, identifed_by))
        self.browser.open(visit.absolute_url())

    def get_actions(self):
        html = lxml.html.fromstring(self.browser.contents)
        xpath = CSSSelector('#plone-contentmenu-actions a span').path
        elements = html.xpath(xpath)
        return [element.text_content().strip() for element in elements]


class TestDeleteAction(ActionTestBase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def setUp(self):
        self.create_user(with_id='hans', with_roles=['Member', 'Contributor'])
        self.create_user(with_id='peter',
                         with_roles=['Member', 'Contributor'])

    def test_user_can_delete_own_contents(self):
        container = self.given_object(titled='Container', creator='hans')
        content = self.given_object(titled='Content',
                                    within=container, creator='peter')

        self.open_browser(visit=content, as_user='peter')
        self.assertIn('Delete', self.get_actions(),
                      'A user should be able to delete his own content.')

    def test_user_can_not_delete_without_delete_objects_on_parent(self):
        container = self.given_object(titled='Container', creator='hans')
        content = self.given_object(titled='Content',
                                    within=container, creator='peter')

        container.manage_permission('Delete objects', roles=[], acquire=False)
        transaction.commit()

        self.open_browser(visit=content, as_user='peter')
        self.assertNotIn('Delete', self.get_actions(),
                         'A user should not be able to delete content'
                         ' without "Delete objects" on the parent.')


class TestCutAction(ActionTestBase):

    layer = testing.COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING

    def setUp(self):
        self.create_user(with_id='hans', with_roles=['Member', 'Contributor'])
        self.create_user(with_id='peter',
                         with_roles=['Member', 'Contributor'])

    def test_user_can_cut_own_contents(self):
        container = self.given_object(titled='Container', creator='hans')
        content = self.given_object(titled='Content',
                                    within=container, creator='peter')

        self.open_browser(visit=content, as_user='peter')
        self.assertIn('Cut', self.get_actions(),
                      'A user should be able to cut his own content.')

    def test_user_can_not_cut_without_delete_objects_on_parent(self):
        container = self.given_object(titled='Container', creator='hans')
        content = self.given_object(titled='Content',
                                    within=container, creator='peter')

        container.manage_permission('Delete objects', roles=[], acquire=False)
        transaction.commit()

        self.open_browser(visit=content, as_user='peter')
        self.assertNotIn('Cut', self.get_actions(),
                         'A user should not be able to cut content'
                         ' without "Delete objects" on the parent.')
