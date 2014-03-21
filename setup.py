from setuptools import setup

setup(
    name='identify_wiki',
    version='0.0.1',
    author='Tristan Chong',
    author_email='tristanchong@gmail.com',
    description='A library for identifying subjects most likely to represent the content of a wiki',
    license='Other',
    packages=['identify_wiki'],
    install_requires=['requests', 'nltk', 'beautifulsoup4']
    )
