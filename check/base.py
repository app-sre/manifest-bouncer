class CheckResult(object):
    """
    Abstract class that represent an check result. Tests should not return this class.
    """

    repr_label = ""

    def __init__(self, manifest, check):
        self.manifest = manifest
        self.check = check

    def manifest_info(self):
        info = []

        try:
            info.append("kind='{}'".format(self.manifest['kind']))
        except KeyError:
            pass

        try:
            info.append("name='{}'".format(self.manifest['metadata']['name']))
        except KeyError:
            pass

        if len(info) > 0:
            return "[{}]".format(", ".join(info))

        return None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = "{}: {}".format(self.repr_label, self.check)

        info = self.manifest_info()
        if info:
            s += info

        return s


class CheckError(CheckResult):
    repr_label = "ERROR"

    def __init__(self, manifest, check, msg):
        super().__init__(manifest, check)
        self.msg = msg

    def __repr__(self):
        s = "{}: {}".format(self.repr_label, self.check)

        info = self.manifest_info()
        if info:
            s += info

        s += ": {}".format(self.msg)

        return s


class CheckSuccess(CheckResult):
    repr_label = 'SUCCESS'


class CheckIgnoreKind(CheckResult):
    """
    Return this is the Check does not apply to that kind. It will not show up in
    the default reports.
    """

    repr_label = 'IGNORE'


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
            if m.startswith('check'):
                f = getattr(cls, m)
                setattr(cls, m, check(f))

                if not hasattr(cls, '_checks'):
                    cls._checks = []

                cls._checks.append(m)

def check(func):
    """
    The check decorator ensures that the check doesn't run and returns
    CheckIgnoreKind if the check doesn't apply to the manifest kind.

    It also ensures that CheckSuccess is returned if no errors are raised
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
