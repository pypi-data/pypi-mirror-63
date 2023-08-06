# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='fipt',
    version='0.1.1',
    description='A python module to analyze fast impedance tortuosity measurements.',
    long_description=readme,
    long_description_content_type='text/markdown',   
    author='Deniz Bozyigit',
    author_email='deniz195@gmail.com',
    url='https://github.com/deniz195/fipt-analysis',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs', 'examples', 'demo_results')),
    install_requires = ['lmfit', 'numpy', 'scipy', ],
    extras_require={
        'dev': [
            'pandas',
            'pytest',
        ], 
    },    
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.6',
      ],    
)
