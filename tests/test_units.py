import pytest

from lib.units import mem_to_bytes, cpu_to_millicores


def test_mem_to_bytes():
    with pytest.raises(Exception):
        assert mem_to_bytes('1 ble')

    with pytest.raises(Exception):
        assert mem_to_bytes('x10 Mi')

    assert mem_to_bytes('10') == 10
    assert mem_to_bytes(10) == 10
    assert mem_to_bytes('1K') == 1000
    assert mem_to_bytes('1Ki') == 1024
    assert mem_to_bytes('2 Ki') == 2048
    assert mem_to_bytes('1M') == 1000000
    assert mem_to_bytes('0.5M') == 500000
    assert mem_to_bytes('12 M') == 12000000
    assert mem_to_bytes('1Mi') == 1048576
    assert mem_to_bytes('0.5 Mi') == 524288
    assert mem_to_bytes('17 Gi') == 18253611008
    assert mem_to_bytes('17 G') == 17000000000


def test_cpu_to_millicores():
    with pytest.raises(Exception):
        assert cpu_to_millicores('1 ble')

    with pytest.raises(Exception):
        assert mem_to_bytes('123.1m')

    assert cpu_to_millicores('1') == 1000
    assert cpu_to_millicores(1) == 1000
    assert cpu_to_millicores('0.01') == 10
    assert cpu_to_millicores('1m') == 1
