from setuptools import find_packages, setup

setup(
    name='toadstool',
    version='0.1.0',
    description='A simple bevy-inspired ecs for python.',
    url="https://github.com/ComLarsic/Toadstool",
    author='ComLarsic',
    author_email="larsjanjensen@protonmail.com",
    license='MIT',
    packages=find_packages(include=["toadstool", "toadstool.*"])
)