import yaml
from textwrap import dedent

from checks.resources import CheckBurstable
from lib.result import CheckError, CheckSuccess


def test_check_burstable_empty_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckBurstable()

    result = c.check_burstable(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_requests_no_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
    """))

    c = CheckBurstable()

    result = c.check_burstable(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_requests_bad_container():
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

    c = CheckBurstable()

    result = c.check_burstable(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_null_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  resources:
                    requests:
                        cpu: null
                        memory: 100
    """))

    c = CheckBurstable()

    result = c.check_burstable(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_empty_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  resources:
                    requests:
                        cpu: ''
                        memory: 100
    """))

    c = CheckBurstable()

    result = c.check_burstable(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_no_limits():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  resources:
                    requests:
                        cpu: 100
                        memory: 100
    """))

    c = CheckBurstable()
    result = c.check_burstable(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_same_limits():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  resources:
                    requests:
                        cpu: 100
                        memory: 100
                    limits:
                        cpu: 200
                        memory: 200
                - name: c2
                  resources:
                    requests:
                        cpu: 100
                        memory: 100
                    limits:
                        cpu: 100
                        memory: 100
    """))

    c = CheckBurstable()
    result = c.check_burstable(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - name: c1
                  resources:
                    requests:
                        cpu: 100
                        memory: 100
                    limits:
                        cpu: 200
                        memory: 200
    """))

    c = CheckBurstable()
    result = c.check_burstable(manifest)
    assert isinstance(result, CheckSuccess)
