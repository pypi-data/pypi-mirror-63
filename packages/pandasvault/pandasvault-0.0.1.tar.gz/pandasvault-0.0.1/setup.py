from setuptools import setup, Command
import os
import sys

setup(name='pandasvault',
      version='0.0.1',
      description='PandasVault - Advanced Pandas Utilities, Functions and Snippets',
      url='https://github.com/firmai/pandasvault',
      author='snowde',
      author_email='d.snow@firmai.org',
      license='MIT',
      packages=['pandasvault'],
      install_requires=[
          'pandas',
          'numpy',
          'sklearn',
          'math'

      ],
      zip_safe=False)
