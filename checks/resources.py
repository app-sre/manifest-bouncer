from lib.base import CheckBase


class CheckResources(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']

    @staticmethod
    def get_containers(m):
        try:
            return m['spec']['template']['spec']['containers']
        except (KeyError, TypeError):
            return []

    @staticmethod
    def do_check_resource(containers, resource, subresource):
        msg = "Expecting {}.{}".format(resource, subresource)
        for c in containers:
            c_name = c.get('name', '<unnamed>')

            try:
                res = c['resources'][resource][subresource]
            except (KeyError, TypeError):
                res = None

            assert res, msg + " in container '{}'.".format(c_name)


class CheckLimits(CheckResources):
    enable_parameter = 'limits'
    description = 'check that limits are defined'
    default_enabled = False

    def check_limits_cpu(self, m):
        containers = self.get_containers(m)
        self.do_check_resource(containers, 'limits', 'cpu')

    def check_limits_memory(self, m):
        containers = self.get_containers(m)
        self.do_check_resource(containers, 'limits', 'memory')


class CheckRequests(CheckResources):
    enable_parameter = 'requests'
    description = 'check that requests are defined'
    default_enabled = False

    def check_requests_cpu(self, m):
        containers = self.get_containers(m)
        self.do_check_resource(containers, 'requests', 'cpu')

    def check_requests_memory(self, m):
        containers = self.get_containers(m)
        self.do_check_resource(containers, 'requests', 'memory')


class CheckBestEffort(CheckResources):
    enable_parameter = 'best-effort'
    description = "ensure containers are best effort (req < limits)"
    default_enabled = True

    def check_best_effort(self, m):
        for container in self.get_containers(m):
            name = container['name']

            resources = container.get('resources', {})
            requests = resources.get('requests', {})
            limits = resources.get('limits', {})

            cpu_req = requests.get('cpu')
            cpu_lim = limits.get('cpu')

            mem_req = requests.get('memory')
            mem_lim = limits.get('memory')

            def error_msg(msg):
                return "{} in container '{}'.".format(msg, name)

            # ensure values are defined
            assert cpu_req, error_msg('Expecting requests/cpu')
            assert cpu_lim, error_msg('Expecting limits/cpu')
            assert mem_req, error_msg('Expecting requests/memory')
            assert mem_lim, error_msg('Expecting limits/memory')

            # ensure reqs is smaller than limits
            assert cpu_req < cpu_lim, error_msg('Expecting cpu_req < cpu_lim')
            assert mem_req < mem_lim, error_msg('Expecting mem_req < mem_lim')
