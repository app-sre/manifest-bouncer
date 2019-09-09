import yaml
from textwrap import dedent

from checks.resources import CheckLimits
from lib.result import CheckError, CheckSuccess


def test_check_limits_empty_containers():
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

    result = c.check_limits_memory(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_limits_no_containers():
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

    result = c.check_limits_memory(manifest)
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
                        memory: 100
    """))

    c = CheckLimits()

    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckError)

    result = c.check_limits_memory(manifest)
    assert isinstance(result, CheckSuccess)


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
                        memory: 100
    """))

    c = CheckLimits()

    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckError)

    result = c.check_limits_memory(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_limits_valid_cpu_no_memory():
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

    result = c.check_limits_memory(manifest)
    assert isinstance(result, CheckError)


def test_check_limits_valid_all():
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
                        memory: 100
    """))

    c = CheckLimits()
    result = c.check_limits_cpu(manifest)
    assert isinstance(result, CheckSuccess)

    result = c.check_limits_memory(manifest)
    assert isinstance(result, CheckSuccess)
