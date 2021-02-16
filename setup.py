from setuptools import setup, find_packages
import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='docrep',
      version='0.3.2',
      description='Python package for docstring repetition',
      long_description=readme(),
      long_description_content_type="text/x-rst",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
      ],
      keywords='docstrings docs docstring napoleon numpy reStructured text',
      url='https://github.com/Chilipp/docrep',
      author='Philipp S. Sommer',
      author_email='philipp.sommer@hzg.de',
      license="Apache-2.0",
      packages=find_packages(exclude=['docs', 'tests*', 'examples']),
      install_requires=[
          'six',
      ],
      data_files=[("", ["LICENSE"])],
      setup_requires=pytest_runner,
      tests_require=['pytest'],
      project_urls={
         'Documentation': 'https://docrep.readthedocs.io',
         'Source': 'https://github.com/Chilipp/docrep',
         'Tracker': 'https://github.com/Chilipp/docrep/issues',
      },
      zip_safe=False)
