#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from linkedin import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

setup(name='linkedin-sdk',
      version=__version__,
      description='Python Interface to the LinkedIn API',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Natural Language :: English',
      ],
      keywords='linkedin python python3',
      author='Harsha Krishnareddy',
      author_email='harsha@ins8s.com',
      maintainer='Harsha Krishnareddy',
      maintainer_email='harsha@ins8s.com',
      url='https://github.com/c0mpiler/linkedin-sdk',
      license='Apache',
      packages=['linkedin'],
      install_requires=['requests>=2.8.1', 'requests-oauthlib>=0.5.0'],
      zip_safe=False
)
