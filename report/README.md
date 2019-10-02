# Report

This directory contains some temporary scripts that will help apply manifest-bouncer on the saasrepos managed by the APPSRE team.

Requirements:
- manifest-bouncer installed
- saasherder installed

Usage:

```bash
# define APP_INTERFACE_USER and APP_INTERFACE_PASSWORD
./get-saas-repos.py | ./clone-saas-repos.sh
./run-manifest-bouncer-saas.sh | tee manifest-bouncer.log
```
