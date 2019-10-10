from lib.base import CheckBase


class CheckRolesAreListedBeforeRoleBindings(CheckBase):
    whitelist = ['List']
    enable_parameter = 'rbac'
    description = 'check that Roles are listed before RoleBindings'
    default_enabled = True

    def check_roles_before_rolebindings(self, m):
        msg = 'RoleBinding "{}" listed before referenced Role "{}"'
        roles = []
        items = m['items']
        for item in items:
            kind = item['kind']
            name = item['metadata']['name']
            if kind == 'Role':
                roles.append(name)
            if kind == 'RoleBinding':
                ref = item['roleRef']
                ref_kind = ref['kind']
                if ref_kind == 'Role':
                    ref_name = ref['name']
                    assert ref_name in roles, msg.format(name, ref_name)
