try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='doubao_crypt',
    version='1.1.0',
    author='biao.xu',
    author_email='biao.xu@baodanyun-inc.com',
    description='doubao crypt python library',
    python_requires=">=3.5.3",
    install_requires=['eciespy', 'requests', 'redis'],
    packages=['doubao_crypt'],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
