import os
from setuptools import setup, find_packages

requirements_txt = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_txt, 'r') as file:
    requirements = file.read().splitlines()

setup(name='JBDB', version="0.1", install_requires=requirements, packages=find_packages())
