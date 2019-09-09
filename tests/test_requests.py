import yaml
from textwrap import dedent

from checks.resources import CheckRequests
from lib.result import CheckError, CheckSuccess


def test_check_requests_empty_containers():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers: []
    """))

    c = CheckRequests()

    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckSuccess)

    result = c.check_requests_memory(manifest)
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

    c = CheckRequests()

    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckSuccess)

    result = c.check_requests_memory(manifest)
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

    c = CheckRequests()

    result = c.check_requests_cpu(manifest)
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
                - resources:
                    requests:
                        cpu: null
                        memory: 100
    """))

    c = CheckRequests()

    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckError)

    result = c.check_requests_memory(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_requests_empty_cpu():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    requests:
                        cpu: ''
                        memory: 100
    """))

    c = CheckRequests()

    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckError)

    result = c.check_requests_memory(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_requests_valid_cpu_no_memory():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    requests:
                        cpu: 100
    """))

    c = CheckRequests()
    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckSuccess)

    result = c.check_requests_memory(manifest)
    assert isinstance(result, CheckError)


def test_check_requests_valid_all():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    spec:
        template:
            spec:
                containers:
                - resources:
                    requests:
                        cpu: 100
                        memory: 100
    """))

    c = CheckRequests()
    result = c.check_requests_cpu(manifest)
    assert isinstance(result, CheckSuccess)

    result = c.check_requests_memory(manifest)
    assert isinstance(result, CheckSuccess)
