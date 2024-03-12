
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='newtonmetrics',
    packages=find_packages(),
    version='0.0.3',
    author='Luca Podo',
    author_email='lucapodo97@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lucapodo/pip-newton.git',
    license='MIT',
    # packages=['newtonmetrics'],
    install_requires=['requests', 'altair', 'termcolor'],
)