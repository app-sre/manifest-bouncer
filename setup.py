from setuptools import find_packages
from setuptools import setup

setup(
    name="manifest-bouncer",
    version="0.1.0",
    license="BSD",

    author="Red Hat App-SRE Team",
    author_email="sd-app-sre@redhat.com",

    description="Run checks on k8s/openshift manifests",

    packages=find_packages(exclude=('tests',)),

    install_requires=[
        "anymarkup>=0.8.0,<0.9.0",
    ],

    python_requires='>=3.7',

    test_suite="tests",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
        'console_scripts': [
            'manifest-bouncer = cli.main:main',
        ],
    },
)
