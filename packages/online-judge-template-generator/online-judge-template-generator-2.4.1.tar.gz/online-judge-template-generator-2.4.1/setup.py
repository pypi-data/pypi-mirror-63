#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='online-judge-template-generator',
    version='2.4.1',
    author='Kimiyuki Onaka',
    author_email='kimiyuki95@gmail.com',
    url='https://github.com/kmyk/online-judge-template-generator',
    license='MIT License',
    description='A simple template generator for competitive programming',
    python_requires='>=3.6',
    install_requires=[
        'appdirs >= 1.4',
        'beautifulsoup4 >= 4.8',
        'Mako >= 1.1',
        'online-judge-tools >= 9',
        'ply >= 3',
        'pyyaml >= 5',
        'requests >= 2.23',
        'sympy >= 1.5',
        'toml >= 0.10',
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        'onlinejudge_template_resources': ['*', 'template/*'],
    },
    entry_points={
        'console_scripts': [
            'oj-template = onlinejudge_template.main:main',
            'oj-contest = onlinejudge_contest.main:main',
        ],
    },
    long_description='',
    long_description_content_type='text/markdown',
)
