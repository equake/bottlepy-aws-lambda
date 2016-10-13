#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='bottlepy_aws_lambda',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    author='Marcos Araujo Sobrinho',
    author_email='marcos@mcmweb.com.br',
    url='http://www.mcmweb.com.br/',
    # scripts=['vivareal/cloudwatch_sqs_metrics.py'],
    long_description=open('README').read(),
    install_requires=open('requirements.txt').read().strip('\n').split('\n')
)
