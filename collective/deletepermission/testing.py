from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from zope.configuration import xmlconfig


class CollectiveDeletepermissionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.deletepermission
        xmlconfig.file('configure.zcml', collective.deletepermission,
                       context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2
        # products, using <five:registerPackage /> in ZCML.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.deletepermission:default')
        setRoles(portal, TEST_USER_ID, ['Manager', 'Contributor'])
        login(portal, TEST_USER_NAME)


COLLECTIVE_DELETEPERMISSION_FIXTURE = CollectiveDeletepermissionLayer()
COLLECTIVE_DELETEPERMISSION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DELETEPERMISSION_FIXTURE, ),
    name="CollectiveDeletepermission:Integration")
COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DELETEPERMISSION_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="CollectiveDeletepermission:Functional")
