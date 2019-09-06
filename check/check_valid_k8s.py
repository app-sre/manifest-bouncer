from .base import CheckBase

class CheckValidK8s(CheckBase):
    _autorun = False

    def check(self, m):
        # it's a dictionary
        assert isinstance(m, dict), 'dictionary type like manifest expected.'

        # it has 'kind'
        assert 'kind' in m, '"kind" key expected.'

        # it has 'apiVersion'
        assert 'apiVersion' in m, '"apiVersion" key expected.'

        # if List: it has 'items'
        if m['kind'] == 'List':
            assert 'items' in m, 'missing "items" key for List objects.'
