import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pip-newton',
    version='0.0.1',
    author='Luca Podo',
    author_email='lucapodo97@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lucapodo/pip-newton.git',
    license='MIT',
    packages=['pip-newton'],
    install_requires=['requests'],
)