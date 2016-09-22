from operator import itemgetter


def upgrade(setup_context):
    """
    The idea is that all roles with "Delete objects" permission should
    also have the "Delete portal content" permission in order to
    actually be able to delete things.
    This principle applies to the site root settings and may be changed
    by workflows, depending on the use case.
    """
    site = setup_context.portal_url.getPortalObject()

    # Make sure that all roles which have the "Delete objects" also have
    # the "Delete portal content" role.
    roles, acquire = get_permission_settings(site, 'Delete portal content')
    for role in get_permission_settings(site, 'Delete objects')[0]:
        if role not in roles:
            roles.append(role)

    site.manage_permission('Delete portal content', roles, acquire=acquire)


def get_permission_settings(context, permission):
    acquire = bool(context.permission_settings(permission)[0]['acquire'])
    roles = map(itemgetter('name'),
                filter(itemgetter('selected'),
                       context.rolesOfPermission(permission)))
    return roles, acquire
