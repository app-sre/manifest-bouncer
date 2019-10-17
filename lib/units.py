import re


def mem_to_bytes(mem):
    if isinstance(mem, (float, int)):
        return mem

    """ https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#meaning-of-memory """
    m = re.match(r"^((?:0|[1-9]\d*)(?:\.\d+)?)\s*([A-Za-z]+)?$", mem)

    if m is None:
        raise Exception("Invalid memory format: {}".format(mem))

    val = float(m.group(1))
    unit = m.group(2)

    if unit is None:
        return int(val)

    units = ['K', 'M', 'G', 'T', 'P', 'E']
    if unit in units:
        return int(val * 10**((units.index(unit) + 1) * 3))

    binary_units = ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei']
    if unit in binary_units:
        return int(val * 1024**(binary_units.index(unit) + 1))

    raise Exception("Unknown unit: {}".format(unit))


def cpu_to_millicores(cpu):
    try:
        m = re.match(r"^([1-9]\d*)m$", cpu)
        if m:
            return int(m.group(1))
    except TypeError:
        pass

    try:
        cores = float(cpu)
    except ValueError:
        raise Exception('Invalid cpu format: {}'.format(cpu))

    return int(cores * 1000)
