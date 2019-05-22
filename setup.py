from setuptools import setup, find_packages
import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='docrep',
      version='0.2.6',
      description='Python package for docstring repetition',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
      ],
      keywords='docstrings docs docstring napoleon numpy reStructured text',
      url='https://github.com/Chilipp/docrep',
      author='Philipp Sommer',
      author_email='philipp.sommer@unil.ch',
      license="GPLv2",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      install_requires=[
          'six',
      ],
      data_files=[("", ["LICENSE"])],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      zip_safe=False)
