try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='doubao_crypt',
    version='1.0',
    author='biao.xu',
    author_email='biao.xu@baodanyun-inc.com',
    description='doubao crypt python library',
    install_requires=['eciespy', 'requests', 'redis'],
    packages=['doubao_crypt']
)
