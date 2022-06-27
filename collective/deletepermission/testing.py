import collective.deletepermission.tests.builders
from ftw.builder.testing import (BUILDER_LAYER, functional_session_factory,
                                 set_builder_session_factory)
from pkg_resources import get_distribution
from plone.app.testing import (PLONE_FIXTURE, TEST_USER_ID, TEST_USER_NAME,
                               FunctionalTesting, PloneSandboxLayer,
                               applyProfile, login, setRoles)

IS_PLONE_5_OR_GREATER = get_distribution('Plone').version >= '5'


class CollectiveDeletepermissionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import collective.deletepermission
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=collective.deletepermission)
        self.loadZCML(package=collective.deletepermission.tests,
                      name='test.zcml')
        if IS_PLONE_5_OR_GREATER:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.deletepermission:default')
        applyProfile(portal, 'collective.deletepermission.tests:dxtests')
        if IS_PLONE_5_OR_GREATER:
            applyProfile(portal, 'plone.app.contenttypes:default')
        setRoles(portal, TEST_USER_ID, ['Manager', 'Contributor'])
        login(portal, TEST_USER_NAME)


COLLECTIVE_DELETEPERMISSION_FIXTURE = CollectiveDeletepermissionLayer()
COLLECTIVE_DELETEPERMISSION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DELETEPERMISSION_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="CollectiveDeletepermission:Functional")
