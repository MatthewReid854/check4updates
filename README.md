![Logo](https://raw.githubusercontent.com/MatthewReid854/check4updates/master/docs/images/logo.png)

[![PyPI version](https://img.shields.io/pypi/v/check4updates?color=brightgreen&logo=Python&logoColor=white&label=PyPI%20package)](https://pypi.org/project/check4updates/)
[![Documentation Status](https://img.shields.io/readthedocs/check4updates/latest.svg?logo=read%20the%20docs&logoColor=white&label=Docs&version=latest)](http://check4updates.readthedocs.io/?badge=latest)
[![Build and Test](https://github.com/MatthewReid854/check4updates/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/MatthewReid854/check4updates/actions/workflows/build_and_test.yml)
[![Codecov](https://codecov.io/github/MatthewReid854/check4updates/badge.svg?branch=main&service=github)](https://codecov.io/github/MatthewReid854/check4updates?branch=main)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MatthewReid854/check4updates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MatthewReid854/check4updates/context:python)
[![Downloads](https://static.pepy.tech/personalized-badge/check4updates?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/check4updates)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?logo=GNU&logoColor=white)](https://mit-license.org/)

*check4updates* is a Python package designed for developers to provide a reliable, simple, and unobtrusive way to check whether their users have the most recent release of their package installed and prompt users when an update is available.

It is recommended that *check4updates* be placed in your package's `__init__.py` file so that it is called every time the package is used. To minimise runtime, *check4updates* only checks online if certain conditions are met, such as sufficient time since the last check. This ensures that incorporating *check4updates* into your Python package will have a negligible (<0.01sec) effect on the time it takes users to import something from your package (which is when `__init__.py` is called) and no impact on any of the functions within your package.

When *check4updates* does check online, it searches PyPI for the most recent release (based on version number) and compares that value with the version installed on the user's system. If certain conditions are met, the user is then prompted to install the updated version which must be done by the user in a separate command so as not to interrupt the currently executing script. Users can choose to upgrade now, skip this version, be reminded later, or never be asked again and *check4updates* will remember this choice and act accordingly.

## Documentation
Detailed documentation and examples are available at [readthedocs](https://check4updates.readthedocs.io/en/latest/).

## Design principles
- periodically check for updates without user action and without slowing down the parent script
- only prompt the user when necessary
- give the user the option to update now, be reminded later, skip this version, or never be asked again
- handle all errors silently to prevent the parent script from being impacted

## Usage
To use *check4updates*, place the following lines in your package's `__init__.py` file:

```python
from check4updates import check_and_prompt
check_and_prompt("your_package")
```

It is as simple as that and *check4updates* will do the rest!

## Contact
If you find any errors, have any suggestions, or would like to request that something be added, please email [alpha.reliability@gmail.com](mailto:alpha.reliability@gmail.com).

If you would like to receive an email notification when a new release of *check4updates* is uploaded to PyPI, [NewReleases.io](https://newreleases.io/) provides this service for free.
