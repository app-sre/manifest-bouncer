from lib.base import CheckBase


class CheckLimits(CheckBase):
    whitelist = ['DeploymentConfig']

    def check_test(self, m):
        pass
