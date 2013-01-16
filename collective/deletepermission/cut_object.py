from AccessControl.Permissions import copy_or_move
from AccessControl import getSecurityManager


def cb_userHasCopyOrMovePermission(self):
    has_copy_or_move = getSecurityManager().checkPermission(copy_or_move, self)
    has_del = getSecurityManager().checkPermission(
        "Delete portal content", self)
    # import ipdb; ipdb.set_trace()
    if has_copy_or_move and has_del:
        return 1
