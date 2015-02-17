from AccessControl import getSecurityManager
from AccessControl.PermissionRole import PermissionRole
from AccessControl.Permissions import copy_or_move


def cb_userHasCopyOrMovePermission(self):
    has_copy_or_move = getSecurityManager().checkPermission(copy_or_move, self)
    has_del = getSecurityManager().checkPermission(
        "Delete portal content", self)
    # import ipdb; ipdb.set_trace()
    if has_copy_or_move and has_del:
        return 1


# Patch manage_cutObjects security.
# By default AT's BaseFolderMixin sets the permission of manage_cutObjects
# to ModifyPortalContent
# We have to change this afterwards.
# Set manage_cutObjects__roles__, which stores the definition generated by
# AccessControl.class_init or App.class_init.
def apply_delete_objects_permission_role(klass, name, replacement):
    setattr(klass, name, PermissionRole('Delete objects', None))


def dummy_replacement():
    pass
