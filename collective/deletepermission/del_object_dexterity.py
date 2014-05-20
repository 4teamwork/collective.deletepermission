from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from plone.dexterity.content import Container


def manage_delObjects(self, ids=None, REQUEST=None):
    """We need to enforce security."""
    sm = getSecurityManager()
    if not sm.checkPermission('Delete objects', self):
        raise Unauthorized(
            "Do not have permissions to remove this object")

    if ids is None:
        ids = []
    if isinstance(ids, basestring):
        ids = [ids]
    for id_ in ids:
        item = self._getOb(id_)
        if not sm.checkPermission("Delete portal content", item):
            raise Unauthorized(
                "Do not have permissions to remove this object")
    return super(Container, self).manage_delObjects(ids, REQUEST=REQUEST)
