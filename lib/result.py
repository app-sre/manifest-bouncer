class CheckResult(object):
    """
    Abstract class that represent an check result. Tests should not return this
    class.
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
    Return this is the Check does not apply to that kind. It will not show up
    in the default reports.
    """

    repr_label = 'IGNORE'
