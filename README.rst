census-map-downloader
=====================

Easily download U.S. census maps


Installation
------------

::

    $ pipenv install census-map-downloader


Command line usage
------------------

::

    Usage: censusmapdownloader [OPTIONS] COMMAND [ARGS]...

      Easily download U.S. census maps

    Options:
      --data-dir TEXT  The folder where you want to download the data
      --help           Show this message and exit.

    Commands:
      counties  Download counties
      places    Download places
      tracts    Download tracts
      zctas      Download ZCTAs
      blocks    Download blocks

Examples
------------------

Here's an example of downloading all counties ::

    censusmapdownloader counties

You can specify the download directory with --data-dir ::

    censusmapdownloader --data-dir ./my-special-folder/ counties

Contributing
------------

Install dependencies for development ::

    $ pipenv install --dev

Run tests ::

    $ make test

Ship new version to PyPI ::

    $ make ship


Developing the CLI
------------------

The command-line interface is implemented using Click and setuptools. To install it locally for development inside your virtual environment, run the following installation command, as `prescribed by the Click documentation <https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration>`_. ::

    $ pip install --editable .
