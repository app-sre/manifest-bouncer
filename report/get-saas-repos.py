#!/usr/bin/env python

import os
import json

import yaml
import requests
from requests.auth import HTTPBasicAuth

saas_repos = set()


def canonical_repo(repo):
    if not repo.endswith('.git'):
        repo += '.git'
    return repo


# APP-INTERFACE
response = requests.get(
    'https://app-interface.devshift.net/graphql',
    params={'query': '{ jenkins_configs_v1 { config } }'},
    auth=HTTPBasicAuth(os.environ['APP_INTERFACE_USER'],
                       os.environ['APP_INTERFACE_PASSWORD']),
    headers={'Content-Type': 'application/json'},
).json()

for jc in response['data']['jenkins_configs_v1']:
    if jc['config']:
        for config in json.loads(jc['config']):
            if config.get('project'):
                if config['project'].get('saas_git'):
                    saas_repos.add(canonical_repo(
                        config['project']['saas_git']))

# CICO

response_yaml = requests.get(
    'https://raw.githubusercontent.com/openshiftio/openshiftio-cico-jobs/master/devtools-ci-index.yaml')
cico = yaml.safe_load(response_yaml.text)

for e in cico:
    if e.get('project'):
        for job_entry in e['project']['jobs']:
            for _, job in job_entry.items():
                if job.get('saas_git'):
                    saas_git = job['saas_git']

                    if ':' in saas_git:
                        saas_git = saas_git[:saas_git.index(':')]

                    saas_org = job.get('saas_organization', 'openshiftio')

                    saas_git = ("https://github.com/{}/{}"
                                .format(saas_org, saas_git))

                    saas_repos.add(canonical_repo(saas_git))

for saas_repo in saas_repos:
    print(saas_repo)
