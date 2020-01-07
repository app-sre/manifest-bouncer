from lib.base import CheckBase
from lib.units import mem_to_bytes, cpu_to_millicores
from lib.utils import get_containers


class CheckResources(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']

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
        containers = get_containers(m, include_init_containers=False)
        self.do_check_resource(containers, 'limits', 'cpu')

    def check_limits_memory(self, m):
        containers = get_containers(m, include_init_containers=False)
        self.do_check_resource(containers, 'limits', 'memory')


class CheckRequests(CheckResources):
    enable_parameter = 'requests'
    description = 'check that requests are defined'
    default_enabled = False

    def check_requests_cpu(self, m):
        containers = get_containers(m, include_init_containers=False)
        self.do_check_resource(containers, 'requests', 'cpu')

    def check_requests_memory(self, m):
        containers = get_containers(m, include_init_containers=False)
        self.do_check_resource(containers, 'requests', 'memory')


class CheckBurstable(CheckResources):
    enable_parameter = 'burstable'
    description = "ensure containers are burstable (req < limits)"
    default_enabled = True

    def check_burstable(self, m):
        for container in get_containers(m, include_init_containers=False):
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

            # ensure reqs are smaller than limits
            cpu_msg = 'Expecting cpu_req ({}) < cpu_lim ({})'.format(
                cpu_req, cpu_lim)

            assert cpu_to_millicores(cpu_req) < cpu_to_millicores(cpu_lim), \
                cpu_msg

            mem_msg = 'Expecting mem_req ({}) < mem_lim ({})'.format(
                mem_req, mem_lim)

            assert mem_to_bytes(mem_req) < mem_to_bytes(mem_lim), mem_msg
