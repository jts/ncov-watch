from setuptools import setup

requirements = ['pysam']

with open('README.md') as rm:
    long_description = rm.read()

setup(
    name="ncov-watch",
    packages=["ncov_watch"],
    version='0.0.1',
    description='Tools for detecting mutations of interest in SARS-CoV-2 sequencing results',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    author='Jared Simpson',
    author_email='jared.simpson@gmail.com',
    zip_safe=False,
    package_data={'ncov_watch': ['watchlists/*']},
    include_package_data=True,
    python_requires=">=3.4",
    url='https://github.com/jts/ncov-watch',
    download_url='https://github.com/jts/ncov-watch/archive/master.zip',

    classifiers=[
        'Development Status :: 3 - Beta',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',  # pathlib is born
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],

    entry_points={
        'console_scripts': [
            'ncov-watch=ncov_watch.ncov_watch:main'  # syntax::  executable=package.module:function
        ]
    }
)
