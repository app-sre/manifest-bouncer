from functools import wraps

from .result import CheckError, CheckIgnoreKind, CheckSuccess, CheckResult


class CheckBase(object):
    _autoregister = True
    _registered = []
    _subclasses = []

    """ only run the check if the manifest 'kind' is in the list """
    whitelist = []

    """
    this check will be enabled if the string in `enable_parameter` is passed as
    an argument
    """
    enable_parameter = None
    description = ""

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._subclasses.append(cls)
        if cls._autoregister:
            cls._registered.append(cls)

        for m in dir(cls):
            if not hasattr(cls, '_checks'):
                cls._checks = []

            if m.startswith('check_'):
                f = getattr(cls, m)
                setattr(cls, m, check(f))

                cls._checks.append(m)


def whitelist(*kinds):
    def whitelisted(func):
        @wraps(func)
        def whitelist_wrapped(self, manifest):
            if kinds and manifest['kind'] not in kinds:
                check_name = "{}:{}".format(self.__class__.__name__,
                                            func.__name__)
                return CheckIgnoreKind(manifest, check_name)
            return func(self, manifest)
        return whitelist_wrapped
    return whitelisted


def check(func):
    """
    This decorator is applied in all the check methods in order to ensure that
    an instance of CheckResult is returned.
    """

    @wraps(func)
    def check_wrapped(self, manifest):
        check_name = "{}:{}".format(self.__class__.__name__, func.__name__)

        if len(self.whitelist) > 0:
            if manifest['kind'] not in self.whitelist:
                return CheckIgnoreKind(manifest, check_name)

        try:
            result = func(self, manifest)
        except AssertionError as e:
            return CheckError(manifest, check_name, str(e))

        if isinstance(result, CheckResult):
            return result

        return CheckSuccess(manifest, check_name)

    return check_wrapped
