from check4updates import check_and_prompt
from distutils.sysconfig import get_python_lib
import os

def cleanup(package_name):
    cwd = os.getcwd()
    package_directory = os.path.join(get_python_lib(), package_name)
    os.chdir(path=package_directory)
    os.remove("check4updates.txt")
    os.chdir(path=cwd)  # reset the current working directory

def test_choice_upgrade():
    package_name = 'requests'
    check_and_prompt(package_name, mock_user_input='1') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='1') # reads the file
    assert result.action == 'remind'
    cleanup(package_name)

def test_choice_remind():
    package_name = 'requests'
    check_and_prompt(package_name, mock_user_input='2') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='2') # reads the file
    assert result.action == 'remind'
    cleanup(package_name)

def test_choice_skip():
    package_name = 'requests'
    check_and_prompt(package_name, mock_user_input='3') # writes the new file
    result = check_and_prompt(package_name, mock_user_input='3') # reads the file
    assert result.action == 'skip'
    cleanup(package_name)


