from setuptools import setup, find_packages

from paperpal import __version__ as version


def slurp(filename):
    with open(filename) as opened_file:
        return opened_file.read()


setup(name='paperpal',
      version=version,
      description='Paper management with Zotero',
      long_description=slurp('README.rst'),
      url='http://github.com/eddieantonio/paperpal',
      entry_points = {
          'console_scripts': ['paperpal=paperpal.__main__:main'],
      },
      author='Eddie Antonio Santos',
      author_email='easantos@ualberta.ca',
      install_requires=slurp('./requirements.txt').split('\n')[:-1],
      license='Apache 2.0',
      packages=['paperpal'],
      package_data={'paperpal': ['*.js']},
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Indexing',
      ]
)
