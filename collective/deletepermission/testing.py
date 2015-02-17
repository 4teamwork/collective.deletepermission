from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
import collective.deletepermission.tests.builders


class CollectiveDeletepermissionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        import collective.deletepermission
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=collective.deletepermission)
        self.loadZCML(package=collective.deletepermission.tests,
                      name='test.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.deletepermission:default')
        applyProfile(portal, 'collective.deletepermission.tests:dxtests')
        setRoles(portal, TEST_USER_ID, ['Manager', 'Contributor'])
        login(portal, TEST_USER_NAME)


COLLECTIVE_DELETEPERMISSION_FIXTURE = CollectiveDeletepermissionLayer()
COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DELETEPERMISSION_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="CollectiveDeletepermission:Functional")
