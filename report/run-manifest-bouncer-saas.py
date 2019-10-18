#!/usr/bin/env python

import os
import datetime

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

date = datetime.datetime.now().strftime("%Y%m%d%H%M")

for (saas_repo_name, url), saas_repo in errors.items():
    log_dir = "saas-repo-logs-{}".format(date)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, saas_repo_name + ".log")

    with open(log_file, 'w') as f:
        f.write("# {}\n\n".format(saas_repo_name))
        f.write("url: {}\n".format(url.decode('utf-8')))
        for context_name, context in saas_repo.items():
            f.write("## {}\n\n".format(context_name))
            for manifest_name, report in context.items():
                f.write("{}:\n".format(manifest_name))
                f.write(report.decode('utf-8'))
                f.write("\n")
