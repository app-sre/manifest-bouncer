import yaml
from textwrap import dedent

from checks.rbac import CheckRolesAreListedBeforeRoleBindings
from lib.result import CheckError, CheckSuccess


def test_roles_before_rolebindings():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: List
    items:
    - apiVersion: rbac.authorization.k8s.io/v1
      kind: Role
      metadata:
        name: test-role
    - apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: test-rolebinding
      roleRef:
        apiGroup: rbac.authorization.k8s.io
        kind: Role
        name: test-role
    """))

    c = CheckRolesAreListedBeforeRoleBindings()

    result = c.check_roles_before_rolebindings(manifest)
    assert isinstance(result, CheckSuccess)


def test_roles_after_rolebindings():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: List
    items:
    - apiVersion: rbac.authorization.k8s.io/v1
      kind: RoleBinding
      metadata:
        name: test-rolebinding
      roleRef:
        apiGroup: rbac.authorization.k8s.io
        kind: Role
        name: test-role
    - apiVersion: rbac.authorization.k8s.io/v1
      kind: Role
      metadata:
        name: test-role
    """))

    c = CheckRolesAreListedBeforeRoleBindings()

    result = c.check_roles_before_rolebindings(manifest)
    assert isinstance(result, CheckError)
