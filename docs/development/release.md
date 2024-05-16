# Creating and Publishing a Release

## Update the Codebase with Release Information

From a local workspace:

### 1. Pull 'main'

    git pull origin main
    git checkout -b "version-X.Y.Z"

### 2. Update setup.py & setup.cfg

Having (and updating) a properly-configured setup.py and setup.cfg supports export to PyPi.

Documentation for setup.cfg:
[declarative config](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html)

### 3. Update Version

Increment the version number appropriately in /__init__.py

### 4. Update the Changelog

Make a section for the version to be released with the contents of the current unreleased section.

Create a new unreleased section above the section to be released.

Example:

Before the update:

```
## Unreleased

### Added

#5 Node health information
#4 Pause polling scheduler
```

After:

```
## Unreleased

## 1.0.1 2024-01-01

### Added

#5 Node health information
#4 Pause polling scheduler
```

### 5. Push to GitHub

    git commit -m "Version increment to X.Y.Z"
    git push --set-upstream origin version-X.Y.Z

## Create a GitHub Release

From GitHub:

### 6. Merge to 'main'

Create a pull request and perform the merge to 'main'.  Once that merge to 'main' has been completed, delete branch 'version-X.Y.Z'.

### 7. Make a Release

Follow GitHub procedures to create a Release. Create a tag and the release description observing conventions from previous releases.

## Push the Release to PyPi

From a local workspace:

### 8. Pull and Check Out 'main' Branch

    git pull origin main

### 9. Build a Distribution Package

    python setup.py sdist bdist_wheel

Documentation: [pypi publish python package](https://realpython.com/pypi-publish-python-package/)

### 10. Publish to PyPI

The Python package 'twine' allows direct interaction with the Python Package Index (PyPI).  Install it and use it to upload the release to PyPI.

    pip install twine
    python3 -m twine upload dist/*

PyPI Credentials will be required.  Please contact the codebase maintainers.
