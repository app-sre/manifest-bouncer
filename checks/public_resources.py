from lib.base import CheckBase


class CheckPublicResources(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']
    whitelist.append('ConfigMap')

    enable_parameter = 'public-resources'
    description = 'check that all data in a resource is public'
    default_enabled = False

    def do_check(self, m, name):
        forbidden_patterns = ["https://"]
        e_msg = f"Resource data should only be public: '{name}'"

        if isinstance(m, str):
            assert not any(fp in m for fp in forbidden_patterns), e_msg
        elif isinstance(m, dict):
            for v in m.values():
                self.do_check(v, name)
        elif isinstance(m, list):
            for i in m:
                self.do_check(i, name)

    def check_public_resource(self, m):
        name = m['metadata']['name']
        self.do_check(m, name)
