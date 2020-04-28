import yaml
from textwrap import dedent

from checks.api_endpoints import CheckDeprecatedAPIEndpoints
from lib.result import CheckError, CheckSuccess


def test_apps_api_endpoint_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
        name: test
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_apps_endpoints(manifest)
    assert isinstance(result, CheckSuccess)


def test_apps_api_endpoint_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps/v1beta1
    kind: Deployment
    metadata:
        name: test
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_apps_endpoints(manifest)
    assert isinstance(result, CheckError)


def test_networking_api_endpoint_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
        name: test
    spec:
        ingress: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_networking_endpoints(manifest)
    assert isinstance(result, CheckSuccess)


def test_networking_api_endpoint_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: extensions/v1beta1
    kind: NetworkPolicy
    metadata:
        name: test
    spec:
        ingress: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_networking_endpoints(manifest)
    assert isinstance(result, CheckError)


def test_policy_api_endpoint_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: policy/v1beta1
    kind: PodSecurityPolicy
    metadata:
        name: test
    spec:
        volumes: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_policy_endpoints(manifest)
    assert isinstance(result, CheckSuccess)


def test_policy_api_endpoint_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: extensions/v1beta1
    kind: PodSecurityPolicy
    metadata:
        name: test
    spec:
        volumes: []
    """))

    c = CheckDeprecatedAPIEndpoints()

    result = c.check_deprecated_policy_endpoints(manifest)
    assert isinstance(result, CheckError)
