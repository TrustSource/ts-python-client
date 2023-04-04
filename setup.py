from setuptools import setup

setup(
    name='ts-python-client',
    python_requires='>=3.8',
    packages=[
        'ts_python_client',
        'ts_python_client.commands'
    ],
    version='2.0.2',
    description='A python client for TrustSource (https://app.trustsource.io) to manage open source code compliance',
    author='EACG GmbH',
    license='Apache-2.0',
    url='https://github.com/trustsource/ts-python-client.git',
    download_url='',
    keywords=['scanning', 'dependencies', 'modules', 'TrustSource'],
    classifiers=[],
    install_requires=[
        'requests',
        'click==8.0.3'
    ],
    scripts=[],
    entry_points={}
)