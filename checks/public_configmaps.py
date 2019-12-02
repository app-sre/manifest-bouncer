from lib.base import CheckBase


class CheckPublicConfigMaps(CheckBase):
    whitelist = ['ConfigMap']

    enable_parameter = 'public-configmaps'
    description = 'check that all data in a ConfigMap is public'
    default_enabled = False

    def check_public_configmap(self, m):
        forbidden_patterns = [
            "https://",
            ".svc.cluster.local",
            "openshift.io",
            "openshift.com",
            "devshift.net",
            "openshiftapps.com",
        ]
        cm_name = m['metadata']['name']
        e_msg = f"ConfigMap data should only be public: '{cm_name}'"

        for v in m.get('data', {}).values():
            assert not any(fp in v for fp in forbidden_patterns), e_msg
