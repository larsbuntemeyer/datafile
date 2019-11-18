from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
  name = 'datafile',         # How you named your package folder (MyLib)
  packages = ['datafile'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='NetCDF data file maintenance',
  long_description=long_description,
  author='Lars Buntemeyer',
  author_email='larsbuntemeyer@gmail.com',
  url='https://github.com/larsbuntemeyer/datafile.git',
  download_url = 'https://github.com/larsbuntemeyer/datafile/archive/v0.1.tar.gz',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'netCDF4'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
