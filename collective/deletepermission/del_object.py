from Products.CMFCore.PortalFolder import PortalFolderBase as PortalFolder
from AccessControl import Unauthorized
from AccessControl import getSecurityManager

def patched_delObject(self, ids=None, REQUEST=None):
    """We need to enforce security."""
    if ids is None:
        ids = []
    if isinstance(ids, basestring):
        ids = [ids]
    for id in ids:
        item = self._getOb(id)
        sm = getSecurityManager()
        if not sm.checkPermission("Delete portal content", item):
            raise Unauthorized, (
                "Do not have permissions to remove this object")
    return PortalFolder.manage_delObjects(self, ids, REQUEST=REQUEST)
