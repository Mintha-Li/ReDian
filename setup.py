from setuptools import setup, find_packages

setup(
    name='Redian',
    version='0.1.0',
    author='Mintha',
    author_email='mintha2002@qq.com',
    description='Redian Processing',
    url='https://github.com/Mintha-Li/ReDian',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'pandas',
        'flask'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
