import yaml
from textwrap import dedent

from checks.registry_quay import CheckRegistryQuay
from lib.result import CheckError, CheckSuccess


def test_check_registry_empty_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_registry_quay_no_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_registry_quay_bad_container():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - bla
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckError)


def test_check_registry_quay_bad_origin():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  image: bla/bla
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckError)


def test_check_registry_quay_bad_origin2():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  image: quay.io/a/b
                - name: c2
                  image: bla/bla
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckError)


def test_check_registry_quay_good():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  image: quay.io/a/b
    """))

    c = CheckRegistryQuay()

    result = c.check_registry_quay(manifest)
    assert isinstance(result, CheckSuccess)
