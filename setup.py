"""Setup for http-server package."""

from setuptools import setup


setup(name='http-server',
      description='Command line program to manage http-server.',
      version=0.1,
      keywords=[],
      classifiers=[],
      author='Will Weatherford',
      author_email='weatherford.william@gmail.com',
      license='MIT',
      packages=[],  # all your python packages with an __init__ file
      py_modules=['server', 'client', 'con_server'],
      package_dir={'': 'src'},
      install_requires=[],
      extras_require={'test': ['pytest', 'pytest-xdist', 'tox']}
      )
