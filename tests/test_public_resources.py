import yaml
from textwrap import dedent

from checks.public_resources import CheckPublicResources
from lib.result import CheckError, CheckSuccess


def test_check_public_resource_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: cm
    data:
        k: http://service:1234
    """))

    c = CheckPublicResources()

    result = c.check_public_resource(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_public_resource_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: cm
    data:
        k: https://example.com
    """))

    c = CheckPublicResources()

    result = c.check_public_resource(manifest)
    assert isinstance(result, CheckError)


def test_check_public_deployment_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
        name: deployment
    spec:
        template:
            spec:
                containers:
                - env:
                    - name: ENV_VAR
                      value: http://service:1234
                image: quay.io/repo/image:latest
                imagePullPolicy: Always
                ports:
                    - containerPort: 4321
                      protocol: TCP
    """))

    c = CheckPublicResources()

    result = c.check_public_resource(manifest)
    assert isinstance(result, CheckSuccess)


def test_check_public_deployment_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
        name: deployment
    spec:
        template:
            spec:
                containers:
                - env:
                      - name: ENV_VAR
                        value: https://example.com
    """))

    c = CheckPublicResources()

    result = c.check_public_resource(manifest)
    assert isinstance(result, CheckError)
