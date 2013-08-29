from AccessControl import getSecurityManager
from AccessControl.Permissions import copy_or_move


# origin: OFS.CopySupport.cb_isCopyable
# Change: the cb_userHasCopyOrMovePermission is patched in .cut_object
# and requires "Delete portal content" so that cutting works as it is
# excpected.
# Since copying should not require "Delete portal content" we directly
# check the permission and no longer use cb_userHasCopyOrMovePermission.
def cb_isCopyable(self):
    # Is object copyable? Returns 0 or 1
    if not (hasattr(self, '_canCopy') and self._canCopy(0)):
        return 0
    # if not self.cb_userHasCopyOrMovePermission():
    if not getSecurityManager().checkPermission(copy_or_move, self):
        return 0
    return 1
