# coding=utf-8
import setuptools


def requirements(filename='requirements.txt'):
    """Returns a list of requirements to install."""
    requires = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                # skip blank lines and comments
                continue
            requires.append(line)

    return requires

setuptools.setup(
    name='ants',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=requirements(),
    description='Ant farm simulator.',
)

