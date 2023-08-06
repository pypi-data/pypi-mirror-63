import re
from setuptools import setup
from io import open

__version__, = re.findall('__version__ = "(.*)"',
                          open('ogc_legends.py').read())


def readme():
    with open('README.rst', "r", encoding="utf-8") as f:
        return f.read()


setup(name='ogc-legends',
      version=__version__,
      description='A small library to work with OGC legends',
      long_description=readme(),
      classifiers=[
          # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools'
      ],
      url='http://github.com/geographika/ogc-legends',
      author='Seth Girvin',
      author_email='sethg@geographika.co.uk',
      license='MIT',
      py_modules=['ogc_legends'],
      install_requires=['owslib'],
      zip_safe=False)
