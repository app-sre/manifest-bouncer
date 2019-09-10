![](https://img.shields.io/github/license/app-sre/qontract-reconcile.svg?style=flat)

# manifest-bouncer

A tool to performs checks on kubernetes/openshift manifests.

## Usage

```
usage: manifest-bouncer [-h] [-v] [--warn-only] [--enable-all]
                        [--enable-limits] [--enable-requests]
                        MANIFEST

Run checks on k8s/openshift manifests.

positional arguments:
  MANIFEST              manifest to check (YAML or JSON). Use '-' to read from
                        STDIN

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print full report
  --warn-only           do not return an error if the checks fail
  --enable-all          run all the checks. To disable a specific check, use
                        the `--disable-<check>` form.
  --enable-limits, --disable-limits
                        check that limits are defined
  --enable-requests, --disable-requests
                        check that requests are defined
```

If all the tests are successful it will exit with `0`. Otherwise it will return with `1` if one or more checks fails.

If the manifest is of `kind: List`, this tool will perform the checks on the list items.

## Adding checks

Checks can be added by simply contributing a new class to the [checks](/checks) directory. The added class must:

- The class name must start with `Check`, typically: `Check<CheckName>`
- It must inherit from `CheckBase` (exported from `lib.base`): `class CheckMyCheck(CheckBase)`.
- If it should be passed only on a specific template `kinds` then it's possible to define a class level attribute `whitelist` that lists all matching kinds.
- Within the class, each method that begins with `check_` will be run as a check. Checks must raise an `AssertionError` if they don't pass, other exceptions will be treated as runtime errors. These methods must have the following signature: `(self, m)`, where `m` is the manifest.
- The `check_` methods can be further filtered for specific kinds using the `@whitelist(*kinds)` decorator.
- Note that you can use the `@whitelist` decorator without the class variable `whitelist` (and viceversa).
- Every class that implements a check should have an `enable_parameter` class varoabñe that will generate two command line options: `--enable-<checkname>` and `--disable-checkname>`. It also requires a `description` class variable.

Example:

```python
from lib.base import CheckBase


class CheckMyCheck(CheckBase):
    whitelist = ["DeploymentConfig", "StatefulSet", "ReplicaSet"]
    enable_parameter = "mycheck"
    help = "check if mycheck passes"

    def check_foo(self, m):
        assert False, "this always fails" # will raise a check failure

    @whitelist("StatefulSet", "ReplicaSet") # this will be run only on the listed kinds
    def check_bar(self, m):
        assert True
```

Since the `enable_parameter` is `my-check` it will generate two new options: `--enable-mycheck` and `--disable-mycheck` (useful along with `--enable-all`).

## Installation

Create and enter the [virtualenv](https://virtualenv.pypa.io/en/latest/) environment:

```sh
python3 -m venv venv
source venv/bin/activate

# make sure you are running the latest setuptools
pip install --upgrade pip setuptools
```

Install the package:

```sh
python setup.py install

# or alternatively use this for a devel environment
python setup.py develop
```

### Requirements

Please see [setup.py](setup.py).

## Licence

[Apache License Version 2.0](LICENSE).

## Authors

These tools have been written by the [Red Hat App-SRE Team](sd-app-sre@redhat.com).
