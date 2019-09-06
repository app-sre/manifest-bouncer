#!/usr/bin/env python

import argparse
import sys

import anymarkup

from check import CheckRunner

# TODO REMOVE
from pprint import pprint

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
    if runner.has_errors():
        runner.error_report(verbose=verbose)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Run checks on k8s/openshift manifests.')

    # verbose
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print full report')

    # limits
    parser.add_argument('--limits', action='store_true',
                        help='Check that limits are defined')

    # manifest path
    parser.add_argument(
        'manifest',
        help="The manifest to check (YAML or JSON). Use '-' to read from STDIN",
        type=read_manifest
    )

    args = parser.parse_args()

    # initialize runner
    runner = CheckRunner(args.manifest)

    # verify it's a valid k8s manifest
    runner.validate_k8s()
    report_and_exit_if_errors(runner, verbose=args.verbose)

    # run checks
    runner.run()

    # display report if errors and exit
    report_and_exit_if_errors(runner, verbose=args.verbose)
