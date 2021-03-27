.. image:: images/logo.png

-------------------------------------

Similar libraries
-----------------

There are many other Python libraries on PyPI which are designed to perform some form of package updating.
These include:

- update-checker
- pip-update
- req-update
- update-check
- esky
- upgrade-requirements
- pip-upgrade
- updater

Most of these libraries are intended for bulk updating all your installed packages. Some are intended for updating a very specific package.
None of these similar libraries overlap with the function and design principles of *check4updates*. These design principles are:

- periodically check for updates without user action and without slowing down the parent script
- only prompt the user when necessary
- give the user the option to update now, be reminded later, skip this version, or never be asked again
- handle all errors silently to prevent the parent script from being impacted
