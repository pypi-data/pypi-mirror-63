[![pipeline status](https://gitlab.com/coopdevs/pyopencell/badges/master/pipeline.svg)](https://gitlab.com/coopdevs/pyopencell/commits/master)
[![coverage report](https://gitlab.com/coopdevs/pyopencell/badges/master/coverage.svg)](https://gitlab.com/coopdevs/pyopencell/commits/master)

> :heart: Inspired by [PyOTRS](https://gitlab.com/rhab/PyOTRS) :heart:

PyOpenCell is a Python wrapper for accessing [Open Cell](https://www.opencellsoft.com/) (Version 6) using the
REST API.

You can see all the API information [here](https://api.opencellsoft.com/6.0.0)

Features
--------

Access an OpenCell instance to:

* find a Customer by ID

Installation
============

Dependencies
------------

Yoy maybe want to create a virtualenv before installing dependencies. 

If you are using `virtualenvwrapper` (https://virtualenvwrapper.readthedocs.io/en/latest/).

* Create virtualenv with python 2.7

```commandline 
$ which python
/usr/bin/python
$ mkvirtualenv --python=/usr/bin/python pyopencell
```
If you are using [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin:
```commandline
$ pyenv virtualenv pyopencell
```

* Install requirements:

```commandline
$ pip install -r requirements.txt
```

Configuration Environment
-------------------------

You need define the OpcenCell API credentials as environment variables. You need define:

```
OPENCELL_BASEURL=<YOUR OC HOST>/opencell
OPENCELL_USER=<YOUR OC USER>
OPENCELL_PASSWORD=<YOUR OC PASSWORD>
```

If this envvars are not defined, a exception will be raised with the name of the envvar not defined.

Python Usage
============

Run test suite
----------

```commandline
$ tox
```

Release process
---

You can upload a new version of pyopencell package to PyPI.
First, you need to load the virtualenv where required python packages are installed.
Be sure that your MR was merged in to `master` and that you have the needed permissions to create a tag and to push to `master` branch. Then, follow the next steps:

1. Checkout to `master` and pull the changes
```commandline
$ git checkout master
$ git pull
```
1. Update the `CHANGELOG.md` file. Modify the `Unreleased` header to point to the new version as is indicated in [keepchangelog.com](https://keepachangelog.com/en/1.1.0/#effort).
1. Update the `VERSION` var in the `setup.py` file.
1. Add, commit and push the changes:
```commandline
$ git add CHANGELOG.md setup.py
$ git commit -m "Bump to 0.x.y"
$ git push
```
1. Run the update:
```commandline
$ python setup.py upload
```

It will create a git tag for the version indicated in `VERSION` variable in `setup.py` and run a pipeline to deploy the package in PyPI.

License
=======
