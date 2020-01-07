from lib.base import CheckBase
from lib.utils import get_containers


class CheckRegistryQuay(CheckBase):
    whitelist = CheckBase.base_kinds['PodTemplateSpec']

    enable_parameter = 'registry-quay'
    description = 'check that all the images are hosted in quay.io'
    default_enabled = True

    def check_registry_quay(self, m):
        e_msg_tpl = "Image should be hosted in quay.io: '{}'"

        for container in get_containers(m):
            e_msg = e_msg_tpl.format(container['image'])
            assert container['image'].startswith('quay.io/'), e_msg
