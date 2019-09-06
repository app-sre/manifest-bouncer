from . import CheckBase


class CheckLimits(CheckBase):
    whitelist = ['DeploymentConfig']

    enable_parameter = 'limits'
    description = 'Check that limits are defined'

    def check_limits_cpu(self, m):
        try:
            containers = m['spec']['template']['spec']['containers']
        except KeyError:
            return

        for c in containers:
            try:
                cpu_limits = c['resources']['limits']['cpu']
            except KeyError:
                cpu_limits = None

            assert cpu_limits, 'Expecting cpu limits'
