from lib.base import CheckBase


class CheckPrometheusRuleSeverity(CheckBase):
    whitelist = ['PrometheusRule']

    enable_parameter = 'prometheus-rule-severity'
    description = 'check that PrometheusRule severity is in allowed values'
    default_enabled = True

    def check_severity(self, m):
        allowed_severities = ['high', 'warning', 'medium', 'info']
        fmt = "[{}/{}/{}] severity '{}' should be one of: {}"

        resource_name = m['metadata']['name']
        groups = m['spec']['groups']
        for group in groups:
            group_name = group['name']
            rules = group['rules']
            for rule in rules:
                alert = rule['alert']
                labels = rule.get('labels', {})
                severity = labels.get('severity', '')
                msg = fmt.format(resource_name,
                                 group_name,
                                 alert,
                                 severity,
                                 allowed_severities)
                assert severity in allowed_severities, msg


class CheckPrometheusRuleLabels(CheckBase):
    whitelist = ['PrometheusRule']

    enable_parameter = 'prometheus-rule-labels'
    description = 'check that required PrometheusRule labels are set'
    default_enabled = True

    def check_labels(self, m):
        required_labels = {'prometheus': 'app-sre', 'role': 'alert-rules'}
        fmt = "[{}] labels should contain: {}"

        resource_name = m['metadata']['name']
        labels = m['metadata'].get('labels', {})

        msg = fmt.format(resource_name, required_labels)
        assert required_labels.items() <= labels.items(), msg
