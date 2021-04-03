from check4updates import check_and_prompt, upgrade
from distutils.sysconfig import get_python_lib
import os
import re
import requests
import pytest

def cleanup(package_name):
    cwd = os.getcwd()
    package_directory = os.path.join(get_python_lib(), package_name)
    os.chdir(path=package_directory)
    try:
        os.remove("check4updates.txt")
    except FileNotFoundError:
        pass
    os.chdir(path=cwd)  # reset the current working directory

def test_packagename_not_str():
    with pytest.raises(ValueError):
        check_and_prompt(package_name=True)

def test_choice_upgrade():
    package_name = 'numpy'
    cleanup(package_name)
    check_and_prompt(package_name, mock_user_input='1') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='1') # reads the file
    assert result.action == 'remind'
    cleanup(package_name)

def test_choice_remind():
    package_name = 'numpy'
    cleanup(package_name)
    check_and_prompt(package_name, mock_user_input='2') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='2') # reads the file
    assert result.action == 'remind'
    cleanup(package_name)

def test_choice_skip():
    package_name = 'numpy'
    cleanup(package_name)
    check_and_prompt(package_name, mock_user_input='3') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='3') # reads the file
    assert result.action == 'skip'
    cleanup(package_name)

def test_choice_neveragain():
    package_name = 'numpy'
    cleanup(package_name)
    check_and_prompt(package_name, mock_user_input='4') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='4') # reads the file
    assert result.action == 'neveragain'
    cleanup(package_name)

def test_upgrade():
    package_name = 'seaborn' # this is used as a test case on GitHub actions which does not have seaborn installed when the VM starts
    out = upgrade(package_name)
    assert out.success == True


