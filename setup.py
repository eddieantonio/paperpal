from paperpal import __version__ as version

def slurp(filename):
    with open(filename) as opened_file:
        return opened_file.read()

from setuptools import setup

setup(name='paperpal',
      version=version,
      description='Helper to export Zotero data',
      long_description=slurp('README.rst'),
      url='http://github.com/eddieantonio/paperpal',
      entry_points = {
          'console_scripts': ['paperpal=paperpal.__init__:main'],
      },
      author='Eddie Antonio Santos',
      author_email='easantos@ualberta.ca',
      install_requires=slurp('./requirements.txt').split('\n')[:-1],
      license='Apache 2.0',
      packages=['paperpal'],
      classifiers=[
        'Development Status :: 3 - Beta',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 2.7',
      ]
)