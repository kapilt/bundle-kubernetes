from setuptools import setup
from setuptools import find_packages
import os

version = '0.1'

with open(os.path.abspath('./README.md')) as readme:
    long_description = readme.read()

setup(name='kubecharm',
      version=version,
      description="Tools releasing and testing kubernetes w/ juju",
      long_description=long_description,
      classifiers=[],
      keywords='kubernetes',
      author='whit',
      author_email='whit.morriss at canonical.com',
      url='',
      license='APL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'path.py',
          'pyyaml',
          'subparse',
          'clint',
          'requests',
      ],

      entry_points="""
      [console_scripts]
      kfc=kubecharm.cli:main
      """,
      )
