#!/usr/bin/env python

import argparse
import sys
import pkgutil
import importlib

import anymarkup

from lib import CheckRunner, CheckBase

# import all checks
checks_path = sys.modules['checks'].__path__
for importer, modname, ispkg in pkgutil.iter_modules(checks_path):
    m = importlib.import_module('checks.{}'.format(modname))


def read_manifest(manifest_file):
    if manifest_file == '-':
        manifest_raw = sys.stdin.read()
        if not manifest_raw:
            raise argparse.ArgumentTypeError("Received empty data from STDIN")
    else:
        try:
            with open(manifest_file) as f:
                manifest_raw = f.read()
        except FileNotFoundError:
            raise argparse.ArgumentTypeError(
                "File not found: {}".format(manifest_file))

    try:
        manifest = anymarkup.parse(manifest_raw, force_types=None)
    except anymarkup.AnyMarkupError:
        raise argparse.ArgumentTypeError(
            "Could not parse file: {}".format(manifest_file))

    return manifest


def report_and_exit_if_errors(runner, verbose=False):
    runner.error_report(verbose=verbose)

    if runner.has_errors():
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Run checks on k8s/openshift manifests.')

    # verbose
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print full report')

    # dynamic test loading
    for cls in CheckBase._subclasses:
        if cls.enable_parameter:
            parser.add_argument(
                '--' + cls.enable_parameter, action='store_true',
                help=cls.description)

    # manifest path
    parser.add_argument(
        'manifest',
        help="The manifest to check (YAML or JSON). "
             "Use '-' to read from STDIN",
        type=read_manifest
    )

    args = parser.parse_args()

    # initialize runner
    runner = CheckRunner(args)

    # verify it's a valid k8s manifest
    runner.validate_k8s()
    report_and_exit_if_errors(runner)

    # run checks
    runner.run()

    # display report if errors and exit
    report_and_exit_if_errors(runner, verbose=args.verbose)
