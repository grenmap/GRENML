#!/bin/bash

# check if flake8 is available
if ! command -v flake8 >/dev/null ; then
    echo "Please install flake8: https://flake8.pycqa.org"
    exit 1
fi

# check if pytest is available
if ! command -v pytest >/dev/null ; then
    echo "Please install pytest: https://docs.pytest.org"
    exit 1
fi

# run flake8
flake8
readonly FLAKE8_STATUS=$?

# run unit tests
pytest
readonly PYTEST_STATUS=$?

if [ "$FLAKE8_STATUS" -gt "0" ] && [ "$PYTEST_STATUS" -gt "0" ] ; then
    echo -n "Please fix the flake8 and the unit test errors "
    echo "before submitting a pull request."
    exit 1
fi

if [ "$FLAKE8_STATUS" -gt "0" ] ; then
    echo "Please fix the flake8 errors before submitting a pull request."
    exit 1
fi

if [ "$PYTEST_STATUS" -gt "0" ] ; then
    echo "Please fix the unit tests errors before submitting a pull request."
    exit 1
fi

echo "Flake8 and unit tests ok."
