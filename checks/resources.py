from lib.base import CheckBase


class CheckResources(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']

    @staticmethod
    def get_containers(m):
        try:
            return m['spec']['template']['spec']['containers']
        except (KeyError, TypeError):
            return

    @staticmethod
    def do_check_resource(containers, resource, subresource):
        msg = "Expecting {}.{}.".format(resource, subresource)
        for c in containers:
            try:
                res = c['resources'][resource][subresource]
            except (KeyError, TypeError):
                res = None

            assert res, msg


class CheckLimits(CheckResources):
    enable_parameter = 'limits'
    description = 'Check that limits are defined'

    def check_limits_cpu(self, m):
        containers = self.get_containers(m)
        if containers:
            self.do_check_resource(containers, 'limits', 'cpu')

    def check_limits_memory(self, m):
        containers = self.get_containers(m)
        if containers:
            self.do_check_resource(containers, 'limits', 'memory')


class CheckRequests(CheckResources):
    enable_parameter = 'requests'
    description = 'Check that requests are defined'

    def check_requests_cpu(self, m):
        containers = self.get_containers(m)
        if containers:
            self.do_check_resource(containers, 'requests', 'cpu')

    def check_requests_memory(self, m):
        containers = self.get_containers(m)
        if containers:
            self.do_check_resource(containers, 'requests', 'memory')
