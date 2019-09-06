from .base import CheckBase

class CheckValidK8s(CheckBase):
    def check(self):
        m = self.manifest

        # it's a dictionary
        if not isinstance(m, dict):
            raise Exception('dictionary type like manifest expected.')

        # it has 'kind'
        if 'kind' not in m:
            raise Exception('"kind" key expected.')

        # it has 'apiVersion'
        if 'apiVersion' not in m:
            raise Exception('"apiVersion" key expected.')

        # if List: it has 'items'
        if m['kind'] == 'List' and 'items' not in m:
            raise Exception('missing "items" key for List objects.')
