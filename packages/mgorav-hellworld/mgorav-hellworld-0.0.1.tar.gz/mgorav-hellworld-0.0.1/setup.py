from setuptools import setup

with open('README.md','r') as file:
    long_description = file.read()

setup(
    name='mgorav-hellworld',
    version='0.0.1',
    description='Say hello!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['hello'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],

)