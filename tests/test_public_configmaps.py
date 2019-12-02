import yaml
from textwrap import dedent

from checks.public_configmaps import CheckPublicConfigMaps
from lib.result import CheckError, CheckSuccess


def test_check_public_configmap_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: cm
    data:
        k: http://service:1234
    """))

    c = CheckPublicConfigMaps()

    result = c.check_public_configmap(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_public_configmap_invalid_https():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: cm
    data:
        k: https://example.com
    """))

    c = CheckPublicConfigMaps()

    result = c.check_public_configmap(manifest)
    assert isinstance(result, CheckError)


def test_check_public_configmap_invalid_domain():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: cm
    data:
        k: openshift.com
    """))

    c = CheckPublicConfigMaps()

    result = c.check_public_configmap(manifest)
    assert isinstance(result, CheckError)
