import sys
import warnings
from AccessControl import getSecurityManager
from AccessControl.Permissions import copy_or_move
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.Dialogs import MessageDialog
from cgi import escape
from OFS.CopySupport import absattr
from OFS.CopySupport import CopyError
from OFS.CopySupport import eNotSupported
from OFS.event import ObjectWillBeMovedEvent
from webdav.Lockable import ResourceLockedError
from ZODB.POSException import ConflictError
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.lifecycleevent import ObjectMovedEvent


def isRenameable(self):
    # Is object renameable? Returns 0 or 1
    if not (hasattr(self, '_canCopy') and self._canCopy(1)):
        return 0
    if hasattr(self, '_p_jar') and self._p_jar is None:
        return 0
    try:    n=aq_parent(aq_inner(self))._reserved_names
    except: n=()
    if absattr(self.id) in n:
        return 0
    if not getSecurityManager().checkPermission(copy_or_move, self):
        return 0
    return 1


# Modified implementation from OFS.CopySupport.CopyContainer
# We do not check for cb_isMoveable() but for our custom isRenameable(),
# which itself does not require "Delete portal content" permission.
def manage_renameObject(self, id, new_id, REQUEST=None):
    """Rename a particular sub-object.
    """
    try:
        self._checkId(new_id)
    except:
        raise CopyError(MessageDialog(
            title='Invalid Id',
            message=sys.exc_info()[1],
            action ='manage_main'))

    ob = self._getOb(id)

    if ob.wl_isLocked():
        raise ResourceLockedError('Object "%s" is locked via WebDAV'
                                    % ob.getId())
    if not isRenameable(ob):
        raise CopyError(eNotSupported % escape(id))
    self._verifyObjectPaste(ob)

    try:
        ob._notifyOfCopyTo(self, op=1)
    except ConflictError:
        raise
    except:
        raise CopyError(MessageDialog(
            title="Rename Error",
            message=sys.exc_info()[1],
            action ='manage_main'))

    notify(ObjectWillBeMovedEvent(ob, self, id, self, new_id))

    try:
        self._delObject(id, suppress_events=True)
    except TypeError:
        self._delObject(id)
        warnings.warn(
            "%s._delObject without suppress_events is discouraged." %
            self.__class__.__name__, DeprecationWarning)
    ob = aq_base(ob)
    ob._setId(new_id)

    # Note - because a rename always keeps the same context, we
    # can just leave the ownership info unchanged.
    try:
        self._setObject(new_id, ob, set_owner=0, suppress_events=True)
    except TypeError:
        self._setObject(new_id, ob, set_owner=0)
        warnings.warn(
            "%s._setObject without suppress_events is discouraged." %
            self.__class__.__name__, DeprecationWarning)
    ob = self._getOb(new_id)

    notify(ObjectMovedEvent(ob, self, id, self, new_id))
    notifyContainerModified(self)

    ob._postCopy(self, op=1)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)
    return None
