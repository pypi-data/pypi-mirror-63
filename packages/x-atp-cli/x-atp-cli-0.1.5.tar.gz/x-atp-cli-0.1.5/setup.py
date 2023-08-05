from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='x-atp-cli',
    version='0.1.5',
    keywords=['x', 'atp', 'test', 'platform'],
    description='X automated test platform command line client',
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    url='https://github.com/hekaiyou/x-atp-cli',
    author="HeKaiYou",
    author_email="hekaiyou@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'x-atp-cli = atp.cli:main'
        ]
    },
)
