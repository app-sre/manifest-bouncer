from .base import CheckBase

class CheckLimits(CheckBase):
    whitelist_kind = ['DeploymentConfig']

    def check(self, m):
        pass
