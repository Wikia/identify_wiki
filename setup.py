from setuptools import setup

setup(
    name='identify_wiki',
    version='0.0.1',
    author='Tristan Chong',
    author_email='tristanchong@gmail.com',
    description='A library for identifying subjects most likely to represent the content of a wiki',
    license='Other',
    packages=['identify_wiki'],
    install_requires=['nlp_services>=0.0.1', 'requests', 'nltk', 'beautifulsoup4'],
    dependency_links=['https://github.com/tristaneuan/nlp_services/archive/master.zip#egg=nlp_services-0.0.1']
    )
