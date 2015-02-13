from plone.dexterity.content import Container
from collective.deletepermission.del_object import protect_del_objects


def manage_delObjects(self, ids=None, REQUEST=None):
    """We need to enforce security."""
    protect_del_objects(self, ids)
    return super(Container, self).manage_delObjects(ids, REQUEST=REQUEST)
