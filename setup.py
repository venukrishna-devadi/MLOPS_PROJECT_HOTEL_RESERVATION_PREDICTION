# in setup.py we will do the project management
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "ML_OPS_Project_1",
    version= "0.1",
    author= "Venu Devadi",
    packages= find_packages(),
    install_requires = requirements
)