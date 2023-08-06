AstroImages FITS Handling routines (astroimages-fits)
=================================
![Version](https://img.shields.io/badge/version-0.2.2-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![PyPI version](https://badge.fury.io/py/astroimages-fits.svg)](https://badge.fury.io/py/astroimages-fits)
![Publish 'astroimages-fits' Package](https://github.com/AstroImages/astroimages-fits/workflows/Publish%20'astroimages-fits'%20Package/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=AstroImages_astroimages-fits&metric=alert_status)](https://sonarcloud.io/dashboard?id=AstroImages_astroimages-fits)

FITS routines and wrappers


Usage
-----

Clone the repo:

    git clone https://github.com/AstroImages/astroimages-fits/
    cd astroimages-fits

Create virtualenv:

    virtualenv -p python3 env
    source env/bin/activate
    pip3 install -r requirements.txt


## Testing

To run unit tests:

    python -m unittest discover test/unit -v


## Packaging

To package
    
    python setup.py sdist

To upload

    pip3 install twine
    twine upload dist/*


## References

### Python Packaging
- https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

### Git actions CICD
- https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

License
-------

MIT, see LICENSE file


