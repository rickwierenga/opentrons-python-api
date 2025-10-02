from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
    name='opentrons_http_api_client',
    version="0.2.0",
    python_requires=">=3.7",
    packages=find_packages(exclude="testing"),
    description='A Python library for interacting with the Opentrons HTTP API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    url='https://github.com/rickwierenga/opentrons-python-api.git',
)
