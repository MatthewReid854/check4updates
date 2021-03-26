.. image:: images/logo.png

-------------------------------------

What is check4updates?
----------------------

*check4updates* is a Python package designed for developers to provide a reliable, simple, and unobtrusive way to check whether their users have the most recent release of their package installed and prompt users when an update is available.
It is recommended that *check4updates* be placed in your package's ``__init__.py`` file so that it is called every time the package is used.
To minimise runtime, *check4updates* only checks online if certain conditions are met, such as sufficient time since the last check.
This ensures that incorporating *check4updates* into your Python package will have a negligible (<0.01sec) effect on the time it takes users to import something from your package (which is when ``__init__.py`` is called) and no impact on any of the functions within your package.
When *check4updates* does check online, it searches PyPI for the most recent release (based on version number) and compares that value with the version installed on the user's system.
If certain conditions are met, the user is then prompted to install the updated version which must be done by the user in a separate command so as not to interrupt the currently executing script.
Users can choose to upgrade now, skip this version, or be reminded later and *check4updates* will remember this choice and act accordingly.

Please see how does *check4updates* work for a more detailed description of its functionality.