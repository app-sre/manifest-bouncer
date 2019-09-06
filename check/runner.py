import sys
import pkgutil
import importlib

from .base import CheckBase, CheckResult, CheckError
from .check_valid_k8s import CheckValidK8s

for importer, modname, ispkg in pkgutil.iter_modules(sys.modules['check'].__path__):
    if modname.startswith('check_'):
        fqdn_module = "check.{}".format(modname)
        if fqdn_module not in sys.modules.keys():
            importlib.import_module('.{}'.format(modname), 'check')


class CheckRunner(object):
    def __init__(self, manifest):
        self.manifest = manifest
        self._results = []

    def run(self):
        if self.manifest['kind'] == 'List':
            for item in self.manifest['items']:
                self.run_item(item)
        else:
            self.run_item(self.manifest)

    def run_item(self, item):
        for cls in CheckBase._registered:
            instance = cls(item)
            for m in cls._checks:
                self.add_result(getattr(instance, m)())

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
        self.add_result(CheckValidK8s(self.manifest).check())

        if self.has_errors():
            return

        if self.manifest['kind'] == 'List':
            for item in self.manifest['items']:
                self.add_result(CheckValidK8s(item).check())
