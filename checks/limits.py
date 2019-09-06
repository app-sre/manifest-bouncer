from lib.base import CheckBase

class CheckLimits(CheckBase):
    whitelist_kind = ['DeploymentConfig']

    def check_test(self, m):
        pass
