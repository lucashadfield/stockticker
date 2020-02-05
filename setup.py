from setuptools import setup, find_packages

setup(
    name='stockticker',
    version='0.1',
    author='Lucas Hadfield',
    packages=find_packages(),
    install_requires=['pandas', 'yfinance', 'notify_run', 'pystache', 'pyyaml'],
    include_package_data=True,
)
