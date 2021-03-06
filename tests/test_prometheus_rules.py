import yaml
from textwrap import dedent

from checks.prometheus_rule import (CheckPrometheusRuleSeverity,
                                    CheckPrometheusRuleLabels)
from lib.result import CheckError, CheckSuccess


def test_prometheus_rule_severity_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
        name: rule
    spec:
        groups:
        - name: group
          rules:
          - alert: alert
            labels:
                severity: high
    """))

    c = CheckPrometheusRuleSeverity()

    result = c.check_severity(manifest)
    assert isinstance(result, CheckSuccess)


def test_prometheus_rule_severity_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
        name: rule
    spec:
        groups:
        - name: group
          rules:
          - alert: alert
            labels:
                severity: critical
    """))

    c = CheckPrometheusRuleSeverity()

    result = c.check_severity(manifest)
    assert isinstance(result, CheckError)


def test_prometheus_rule_labels_valid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
        name: rule
        labels:
            prometheus: app-sre
            role: alert-rules
    """))

    c = CheckPrometheusRuleLabels()

    result = c.check_labels(manifest)
    assert isinstance(result, CheckSuccess)


def test_prometheus_rule_labels_invalid():
    manifest = yaml.safe_load(dedent("""
    ---
    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
        name: rule
        labels:
            promethues: app-sre
            role: alert-rules
    """))

    c = CheckPrometheusRuleLabels()

    result = c.check_labels(manifest)
    assert isinstance(result, CheckError)
