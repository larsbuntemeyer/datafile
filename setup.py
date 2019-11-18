from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='datafile',
      version='0.0.1',
      description='common NetCDF data file maintenance routines',
      url='https://github.com/larsbuntemeyer/datafile.git',
      author='Lars Buntemeyer',
      author_email='larsbuntemeyer@gmail.com',
      license='MIT',
      packages=['datafile'],
      long_description=long_description,
      zip_safe=False)
