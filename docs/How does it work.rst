.. image:: images/logo.png

-------------------------------------

How does it work?
-----------------

check4updates only contains two classes. One of these is `check_and_prompt()` and the other is `upgrade()`. These are discussed below:

check4updates.check_and_prompt()
''''''''''''''''''''''''''''''''

Remember to include *check4updates* in your package's requirements.
To use *check4updates*, place the following lines in your package's ``__init__.py`` file:

.. code:: python

    from check4updates import check_and_prompt
    check_and_prompt("your_package")

Each time your users import something from your package, the ``check_and_prompt`` command is executed. This command does the following:

1. Check if there is a record of a previous action by searching the package's package folder (where ``__init__.py`` is located) for the file "check4updates.txt".

2. If "check4updates.txt" is not found, go to (3) else go to (6).

3. *check4updates* will use the requests library to search PyPI for the latest version and check which version the user currently has installed. If there is an error in getting the PyPI version go to (8) else if the PyPI version is obtained successfully, *check4updates* will compare the versions to determine whether an update is available. If an update is available go to (4) else go to (5).

4. When an update is available, prompt the user with the following:

    .. code-block:: console
    
        Version 0.2.1 of example_package is available on PyPI
        You currently have version 0.1.9 of example_package installed
        Please choose an option:
        1. I want to upgrade
        2. Remind me tomorrow
        3. Skip this version
        4. Never ask me again
        Your choice: 

The user's choices will trigger the following:

- Update now :math:`\Rightarrow` Instructions will be printed to the console on how to update. See below for text outputs.
- Remind me later :math:`\Rightarrow` *check4updates* will store the current timestamp and the action to "remind" in the "check4updates.txt" file and place this in the package folder. This is the file that is checked in step (1).
- Skip this version :math:`\Rightarrow` *check4updates* will store the current time and the action to "skip" in the "check4updates.txt" file and place this in the package folder. This is the file that is checked in step (1). END
- Never ask me again :math:`\Rightarrow` *check4updates* will store "neveragain" in the "check4updates.txt" file. This will be remembered even if the user updates the package manually. END

5. If no update is available, *check4updates* will store the current time and the action "checked" in the "check4updates.txt" file and place this in the package folder. This ensures that the time of the last check is recorded and will be found in step (1) on the next execution. END

6. The file "check4updates.txt" contains 4 pieces of information on a single line separated by spaces. These are "action timestamp PyPI_version count". When *check4updates* is found to contain these actions, the following steps will be taken:

- checked - determine how much time has passed between the timestamp of the last check and now. If sufficient time has passed (as determined by the "online_check_interval" argument) then another check will be performed. Go to (3) else END.
- remind - determine how much time has passed between the timestamp of the last prompt and now. If sufficient time has passed (as determined by the "remind_delay" argument) then another check will be performed (in case a new version was released since the last prompt). Go to (3) else END.
- skip - determine how much time has passed between the timestamp of the last check and now. If sufficient time has passed (as determined by the "online_check_interval" argument) then another check will be performed. This ensures that check4updates continues to periodically check PyPI for a new version when the user has selected to skip the current version. *check4updates* will use the requests library to search PyPI for the latest version and check whether the latest version from PyPI exceeds the PyPI_version stored in "check4updates.txt". If there is an error in getting the PyPI version go to (8) else if a new version (beyond the skipped version) is available then go to (4) else go to (7).
- neveragain - No further action will be taken as the user has previously decided never to be asked again. END
- connectionerror - This means *check4updates* has previously tried to seach online in step (3) and has encountered a problem with the connection (likely due to not being connected to the internet). In this case the action was recorded as connectionerror. Another check will be performed if sufficient time has passed (as determined by the "check_interval" argument). Note that the count is used to increase the value of the "online_check_interval" argument if there have been repeated failed connection attempts. This is intended to reduce the number of attempts to check PyPI when failure seems likely. END

7. As the user has selected to skip the current PyPI version, update the timestamp so that the next time (6) is run it will only check online if sufficient time has passed. END

8. If there is an error in getting the PyPI version then "check4updates.txt" will have connectionerror recorded in the action, the current timestamp, 0.0.0 as the PyPI version, and 1 added to the current count. END

The flowchart below shows the above description in an abbreviated form.

.. image:: images/flowchart_not_ready_yet.png

check4updates.upgrade()
'''''''''''''''''''''''

``check4updates.upgrade()`` provides a simple way of updating a package from within a new Python script.
The option to use `upgrade()` is provided in step (4) if the user selects "update now".
To run `upgrade()` from within a script, type the following:

.. code:: python

    from check4updates import upgrade
    upgrade("your_package")

When this command is run it calls pip as a subprocess and passes the "your_package" argument.
This is the python script equivalent to typing in your command prompt or terminal.

.. code-block:: console

    pip install --upgrade your_package

The output from pip that you would normally get in your command prompt or terminal is printed to your IDE's console.

Error handling
''''''''''''''

*check4updates* is designed to never impact the runtime of the parent script.
*check4updates* achieves this by handling errors silently, ensuring the user will never receive an error (such as no internet connection when trying to check online).
This gives developers the confidence that using *check4updates* in their packages will never result in their package being crashed by *check4updates*, thereby avoiding negative user experiences.

The one downside to this is error reporting (to the user) from *check4updates* is non-existent.
This means that if *check4updates* does run into trouble then you will probably never know.
Your users would only know if they were diligent enough to check whether an update was available and to note that *check4updates* was part of the ``__init__.py`` file but they were not receiving a prompt to update.
This could impact some of your users (based on their unique system configuration) but the worst case scenario (of failing to notify users of an update) is equivalent to not using *check4updates* at all.

In accordance with the `MIT license <https://github.com/MatthewReid854/check4updates/blob/main/LICENSE>`_, the author of *check4updates* provides no guarantees or assurances that the use of this software will not cause errors. All effort has been made to ensure the software is free of errors, however, the software is provided "as is", without warranty of any kind, express or implied.

Text outputs
''''''''''''

When the user is prompted for their choice, they receive the following text:

.. code-block:: console

    Version 0.2.1 of example_package is available on PyPI
    You currently have version 0.1.9 of example_package installed
    Please choose an option:
    1. I want to upgrade
    2. Remind me tomorrow
    3. Skip this version
    4. Never ask me again
    Your choice: 

The following text outputs will be printed to the console when the user selects 1, 2, 3, or 4 from the prompt:

- 1.

    .. code-block:: console
    
        To upgrade example_package you can do one of the following:
        Open your command prompt / terminal and type: pip install --upgrade example_package
        or
        From within your Python IDE in a new Python script type:
        from check4updates import upgrade
        upgrade('example_package')
        Then run the script and example_package will be upgraded to the most recent version.

- 2.
    
    .. code-block:: console
    
        You will be reminded again tomorrow or the next time you use example_package
        To upgrade to version 0.2.1 manually, please use: pip install --upgrade example_package

- 3.
    
    .. code-block:: console
    
        Version 0.2.1 of example_package will be skipped
        You will be prompted again when the next version of example_package is released
        To upgrade to version 0.2.1 manually, please use: pip install --upgrade example_package

- 4.
    
    .. code-block:: console
    
        You will never again be prompted to upgrade example_package, even if you upgrade manually.
        To upgrade to version 0.2.1 manually, please use: pip install --upgrade example_package
