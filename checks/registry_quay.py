from lib.base import CheckBase


class CheckRegistryQuay(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']

    enable_parameter = 'registry-quay'
    description = 'check that all the images are hosted in quay.io'
    default_enabled = True

    @staticmethod
    def get_containers(m):
        try:
            return m['spec']['template']['spec']['containers']
        except (KeyError, TypeError):
            return []

    def check_registry_quay(self, m):
        e_msg_tpl = "Image should be hosted in quay.io: '{}'"

        for container in self.get_containers(m):
            e_msg = e_msg_tpl.format(container['image'])
            assert container['image'].startswith('quay.io/'), e_msg
