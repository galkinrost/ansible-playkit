#!/usr/bin/env python

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("PlayKit now needs setuptools in order to build.")
    sys.exit(1)

setup(name='ansible-playkit',
      version='1.0.0',
      description='Ansible deploy without bullshit. Thin wrapper around Docker to run ansible and openssl.',
      author='Oleg Poyaganov',
      author_email='oleg@poyaganov.com',
      url='https://github.com/opedge/ansible-playkit',
      license='MIT',
      install_requires=['setuptools'],
      package_dir={ '': 'lib' },
      packages=find_packages('lib'),
      package_data={
          '': ['Dockerfile', 'project_template/**/*'],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Installation/Setup',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
      ],
      scripts=[
          'bin/ansible-playkit',
      ],
      data_files=[],
)