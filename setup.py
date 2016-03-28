import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
VERSION = open(os.path.join(here, 'VERSION')).read()

requires = [
    'Pillow',
    'six',
    'easy-thumbnails'
]

setup(name='django-skd-crop',
      version=VERSION,
      description='Easy working with images and crop',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Framework :: Django",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='SteelKiwi',
      url='https://github.com/steelkiwi/django-skd-crop',
      keywords='web django crop image field',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires)
