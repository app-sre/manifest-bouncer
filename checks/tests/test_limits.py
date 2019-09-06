import yaml
from textwrap import dedent

from checks.limits import CheckLimits
from lib.result import CheckError, CheckSuccess


def test_check_limits_cpu_empty_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_limits_cpu_no_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_limits_bad_container():
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

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckError)


def test_check_limits_null_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    limits:
                        cpu: null
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckError)


def test_check_limits_empty_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    limits:
                        cpu: ''
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckError)


def test_check_limits_valid_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    limits:
                        cpu: 100
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckSuccess)
