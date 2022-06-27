from operator import itemgetter

from six.moves import filter, map


def upgrade(setup_context):
    site = setup_context.portal_url.getPortalObject()
    roles, acquire = get_permission_settings(site, 'Delete portal content')
    if 'Site Administrator' not in roles:
        roles.append('Site Administrator')

    site.manage_permission('Delete portal content', roles, acquire=acquire)


def get_permission_settings(context, permission):
    acquire = bool(context.permission_settings(permission)[0]['acquire'])
    roles = list(map(itemgetter('name'),
                list(filter(itemgetter('selected'),
                       context.rolesOfPermission(permission)))))
    return roles, acquire
