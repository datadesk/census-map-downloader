import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='census-map-downloader',
    version='0.0.2',
    description="Easily download U.S. census maps",
    long_description=read('README.rst'),
    author='Los Angeles Times Data Desk',
    author_email='datadesk@latimes.com',
    url='http://www.github.com/datadesk/census-map-downloader',
    license="MIT",
    packages=(
        "census_map_downloader",
        "census_map_downloader.geotypes",
    ),
    install_requires=(
        "geopandas",
        "us",
        "click"
    ),
    entry_points="""
        [console_scripts]
        censusmapdownloader=census_map_downloader.cli:cmd
    """,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Maintainer': 'https://github.com/datadesk',
        'Source': 'https://github.com/datadesk/census-map-downloader',
        'Tracker': 'https://github.com/datadesk/census-map-downloader/issues'
    },
)
