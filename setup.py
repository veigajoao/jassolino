from setuptools import setup, find_packages

setup(
    name='my-cli-tool',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'my-cli=jassolino_cli.cli:hello',
        ],
    },
)