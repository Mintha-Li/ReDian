from setuptools import setup, find_packages

setup(
    name='热点处理器',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'pandas',
        'flask'
    ],
)
