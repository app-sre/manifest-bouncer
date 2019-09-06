from lib.base import CheckBase, whitelist


class CheckValidK8s(CheckBase):
    _autoregister = False

    def check_dictionary(self, m):
        # it's a dictionary
        assert isinstance(m, dict), 'dictionary type like manifest expected.'

    def check_kind(self, m):
        # it has 'kind'
        assert 'kind' in m, '"kind" key expected.'

    def check_api_version(self, m):
        # it has 'apiVersion'
        assert 'apiVersion' in m, '"apiVersion" key expected.'

    @whitelist('List')
    def check_list_items(self, m):
        assert 'items' in m, 'missing "items" key for List objects.'
