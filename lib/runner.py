import sys
import pkgutil
import importlib

from .base import CheckBase
from .result import CheckResult, CheckError
from checks.valid_k8s import CheckValidK8s

# import all checks
checks_path = sys.modules['checks'].__path__
for importer, modname, ispkg in pkgutil.iter_modules(checks_path):
    fqdn_module = "checks.{}".format(modname)
    if fqdn_module not in sys.modules.keys():
        importlib.import_module(fqdn_module)


class CheckRunner(object):
    def __init__(self, args):
        self.args = args
        self.manifest = self.args.manifest
        self._results = []

    def run(self, classes=None, manifest=None, split_list=True):
        if not manifest:
            manifest = self.manifest

        if split_list and manifest['kind'] == 'List':
            for item in manifest['items']:
                self.run_item(item, classes)
        else:
            self.run_item(manifest, classes)

    def run_item(self, item, classes=None):
        if not classes:
            classes = []

            for cls in CheckBase._registered:
                if not cls.enable_parameter:
                    continue

                is_enabled = getattr(self.args, cls.enable_parameter)

                if self.args.disable_all:
                    if is_enabled:
                        classes.append(cls)
                elif self.args.enable_all:
                    if is_enabled is not False:
                        classes.append(cls)
                else:
                    if is_enabled or cls.default_enabled:
                        classes.append(cls)

        for cls in classes:
            instance = cls()
            for m in cls._checks:
                m = getattr(instance, m)
                self.add_result(m(item))

    def add_result(self, result):
        if isinstance(result, CheckResult):
            self._results.append(result)
        else:
            raise Exception("Invalid check return")

    def errors(self):
        return filter(lambda o: isinstance(o, CheckError), self._results)

    def has_errors(self):
        return len(list(self.errors())) > 0

    def error_report(self, verbose=False):
        if verbose:
            for e in self._results:
                print(e)
        else:
            for e in self.errors():
                print(e)

    def validate_k8s(self):
        self.run(classes=[CheckValidK8s], split_list=False)

        if self.has_errors():
            return

        if self.manifest['kind'] == 'List':
            self.run(classes=[CheckValidK8s])
