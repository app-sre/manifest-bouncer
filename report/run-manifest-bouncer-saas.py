#!/usr/bin/env python

import os

import sh
import yaml


WORK_DIR = 'saas-repos'

errors = {}

for saas_repo in os.listdir(WORK_DIR):

    saas_repo_path = os.path.join(WORK_DIR, saas_repo)
    config = yaml.safe_load(open(os.path.join(saas_repo_path, 'config.yaml')))

    git_dir = os.path.join(saas_repo_path, '.git')
    repo_url = sh.git('--git-dir', git_dir, 'config',
                      '--get', 'remote.origin.url').stdout

    for context in config['contexts']:
        context_name = context['name']

        output_dir = os.path.join(saas_repo_path,
                                  context['data']['output_dir'])

        for manifest in os.listdir(output_dir):
            manifest_path = os.path.join(output_dir, manifest)
            report = sh.manifest_bouncer('--warn-only', manifest_path)

            if report:
                errors.setdefault((saas_repo, repo_url), {})
                errors[(saas_repo, repo_url)].setdefault(context_name, {})
                errors[(saas_repo, repo_url)][context_name][manifest] = \
                    report.stdout

for (saas_repo_name, url), saas_repo in errors.items():
    print("# {}\n".format(saas_repo_name))
    print("url: {}\n".format(url.decode('utf-8')))
    for context_name, context in saas_repo.items():
        print("## {}\n".format(context_name))
        for manifest_name, report in context.items():
            print("*{}*\n".format(manifest_name))
            print("```")
            print(report.decode('utf-8'))
            print("```\n")
