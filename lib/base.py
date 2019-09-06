from .result import CheckError, CheckIgnoreKind, CheckSuccess

class CheckBase(object):
    _autorun = True
    _registered = []

    """ only run the check if the manifest 'kind' is in the list """
    whitelist_kind = []

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._autorun:
            cls._registered.append(cls)

        for m in dir(cls):
            if not hasattr(cls, '_checks'):
                cls._checks = []

            if m.startswith('check_'):
                f = getattr(cls, m)
                setattr(cls, m, check(f))

                cls._checks.append(m)

def check(func):
    """
    This decorator is applied in all the check methods in order to ensure that
    an instance of CheckResult is returned.
    """

    def check_wrapped(self, manifest):
        check_name = "{}:{}".format(self.__class__.__name__, func.__name__)

        if len(self.whitelist_kind) > 0:
            if manifest['kind'] not in self.whitelist_kind:
                return CheckIgnoreKind(manifest, check_name)

        try:
            func(self, manifest)
        except AssertionError as e:
            return CheckError(manifest, check_name, str(e))

        return CheckSuccess(manifest, check_name)

    return check_wrapped
