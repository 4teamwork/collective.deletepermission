from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from Products.CMFCore.PortalFolder import PortalFolderBase as PortalFolder


def protect_del_objects(self, ids=None):
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


def manage_delObjects(self, ids=None, REQUEST=None):
    """We need to enforce security."""
    protect_del_objects(self, ids)
    return PortalFolder.manage_delObjects(self, ids, REQUEST=REQUEST)
