def get_containers(manifest, include_init_containers=True):
    if manifest['kind'] == 'CronJob':
        template = manifest['spec']['jobTemplate']['spec']['template']
    else:
        template = manifest['spec']['template']

    containers = []
    try:
        containers.extend(template['spec']['containers'])
    except (KeyError, TypeError):
        pass

    if not include_init_containers:
        return containers

    try:
        containers.extend(template['spec']['initContainers'])
    except (KeyError, TypeError):
        pass

    return containers
