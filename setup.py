from setuptools import setup, find_packages

setup(
    name='bitbucketcli',
    version='0.1.5',
    description='A command line interface for working with Bitbucket.',
    author='James Scheiber',
    author_email='jscheiber22@gmail.com',
    packages=find_packages(include=['bitbucketcli', 'bitbucketcli.*']),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ],
    entry_points={
        "console_scripts": [
            "bitbucketcli = bitbucketcli.__main__:main"
        ]}
)
