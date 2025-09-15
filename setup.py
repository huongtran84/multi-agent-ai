from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MULTI AGENT",
    version="0.1",
    author="huongtd",
    packages=find_packages(),
    install_requires = requirements,
)