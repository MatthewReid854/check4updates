# -*- coding: utf-8 -*-
# pylint: skip-file

__title__ = "check4updates"
__version__ = "0.0.2"
__description__ = "Check if an updated package is available and prompt users to upgrade"
__url__ = "https://github.com/MatthewReid854/check4updates"
__author__ = "Matthew Reid"
__author_email__ = "alpha.reliability@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2021 Matthew Reid"


import time
import os
from distutils.sysconfig import get_python_lib


class upgrade:
    def __init__(self, package_name):
        import sys
        import subprocess

        if type(package_name) is not str:
            raise ValueError("package_name must be a string")
        self.package_name = package_name
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", self.package_name]
        )
        self.success = True  # for test purposes to confirm this code ran correctly


class check_and_prompt:
    """
    :param package_name: string - the package name. e.g. 'matplotlib'
    :param remind_delay: int - number of seconds until next reminder - default is 86400 (1 day)
    :param online_check_interval: int - number of seconds until we look online again to check the current PyPI version - default is 6048000 (7 days)
    :param mock_user_input: string. Used to mock the user input when running automated tests. Must be None or '1','2','3','4'
    """

    def __init__(
        self,
        package_name,
        remind_delay=86400,
        online_check_interval=6048000,
        mock_user_input=None,
    ):
        self.package_name = package_name

        start_time = time.time()  # used for timing the execution of this script
        prompt_delay = 0

        # here we need to read the check4updates.txt file and determine whether we need to check online
        # only look online if it has been enough time since the last check because checking takes time so we don't want to do it too often
        cwd = os.getcwd()  # get the current directory so we can reset it later
        package_directory = os.path.join(get_python_lib(), self.package_name)
        os.chdir(path=package_directory)
        check_and_prompt.read_file(self)
        delta_time = time.time() - float(self.timestamp)

        # Increase online check interval every 10 successive connection failures
        if self.action == "connectionerror" and self.count > 10:
            multiplier = 0.1 * self.count
        else:
            multiplier = 1

        if self.action is None:
            check_online_version = True
        elif (
            self.action in ["checked", "connectionerror"]
            and delta_time > online_check_interval * multiplier
        ):
            check_online_version = True
        elif self.action == "remind" and delta_time > remind_delay:
            check_online_version = True  # get the pypi version again in case it has been updated since the last reminder
        elif self.action == "skip" and delta_time > online_check_interval * multiplier:
            check_online_version = (
                True  # get the pypi version again to see if the skip condition is met
            )
        else:
            check_online_version = False
            # if we are not checking the online version then we can not continue with any update process

        if check_online_version is True:
            check_and_prompt.get_pypi_version(self)
            check_and_prompt.get_installed_version(self)

            if self.pypi_version != "connectionerror":
                # we can only proceed if obtaining the pypi version was successful

                # pad the versions such that if one version is 1.2.3 and the other is 1.2 the shorter one will be padded to 1.2.0
                # further pad each part of the version to 5 digits so 2.51.3 and 5.1.1 aren't just 2513 vs 511 as 5.1.1 should be larger.
                # Instead they are padded to 5 digits anc concatenated so 5.1.1 becomes 000050000100001 which allows for easy numerical comparison (hence the need for padding)
                pypi_version_split = self.pypi_version.split(".")
                pypi_version_length = len(pypi_version_split)
                installed_version_split = self.installed_version.split(".")
                installed_version_length = len(installed_version_split)
                decision_version_split = self.version.split(
                    "."
                )  # the decision version is the latest pypi version at the time of the last decision. Only used for 'skip'
                decision_version_length = len(decision_version_split)

                max_version_length = max(
                    installed_version_length,
                    pypi_version_length,
                    decision_version_length,
                )

                installed_version_split.extend(
                    ["0"] * (max_version_length - installed_version_length)
                )
                installed_version_numeric = int(
                    check_and_prompt.pad_zeros(installed_version_split)
                )

                pypi_version_split.extend(
                    ["0"] * (max_version_length - pypi_version_length)
                )
                pypi_version_numeric = int(
                    check_and_prompt.pad_zeros(pypi_version_split)
                )

                decision_version_split.extend(
                    ["0"] * (max_version_length - decision_version_length)
                )
                decision_version_numeric = int(
                    check_and_prompt.pad_zeros(decision_version_split)
                )

                # check if installed version has been superseded
                if installed_version_numeric == pypi_version_numeric:
                    # write the timestamp of the current check to auto_update.txt "checked timestamp_of_check pypi_version"
                    check_and_prompt.write_file(self, "checked")
                else:  # version is outdated
                    if (
                        self.action == "skip"
                        and pypi_version_numeric == decision_version_numeric
                    ):  # user has already chosen to skip this version
                        check_and_prompt.write_file(
                            self, "skip"
                        )  # update the timestamp so we don't check for another week
                    else:
                        line = "----------------------------------------------------------------------------------"
                        # prompt the user to update
                        check_and_prompt.printred(line, bold=True)
                        check_and_prompt.printred(
                            "Version ",
                            self.pypi_version,
                            " of ",
                            self.package_name,
                            " is available on PyPI",
                        )
                        check_and_prompt.printred(
                            "You currently have version ",
                            self.installed_version,
                            " of ",
                            self.package_name,
                            " installed",
                        )

                        prompt_choice = 0
                        time_before_prompt = time.time()
                        while prompt_choice not in ["1", "2", "3", "4"]:
                            check_and_prompt.printred("Please choose an option:")
                            check_and_prompt.printred("1. I want to upgrade")
                            check_and_prompt.printred("2. Remind me tomorrow")
                            check_and_prompt.printred("3. Skip this version")
                            check_and_prompt.printred("4. Never ask me again")
                            if mock_user_input is None:
                                red, endred = "\033[91m", "\033[0m"
                                prompt_choice = input(
                                    str(red + "Your choice: " + endred)
                                )
                            else:
                                # accept the mocked user input
                                prompt_choice = mock_user_input

                            if prompt_choice not in ["1", "2", "3", "4"]:
                                check_and_prompt.printred("Invalid choice.")
                        prompt_delay = time.time() - time_before_prompt

                        italics = "\033[3m"
                        if prompt_choice == "1":
                            # if mock_user_input is None:
                            check_and_prompt.printred(
                                "\nTo upgrade ",
                                self.package_name,
                                " you can do one of the following:",
                            )
                            check_and_prompt.printred(
                                "Open your command prompt / terminal and type:",
                                italics,
                                " pip install --upgrade ",
                                self.package_name,
                            )
                            check_and_prompt.printred("or")
                            check_and_prompt.printred(
                                "From within your Python IDE in a new Python script type:\n"
                                + italics
                                + "from check4updates import upgrade\nupgrade('"
                                + self.package_name
                                + "')"
                            )
                            check_and_prompt.printred(
                                "Then run the script and ",
                                self.package_name,
                                " will be upgraded to the most recent version.",
                            )
                            check_and_prompt.printred(line, "\n", bold=True)
                            check_and_prompt.write_file(self, "remind")
                        elif prompt_choice == "2":
                            check_and_prompt.printred(
                                "\nYou will be reminded again tomorrow or the next time you use ",
                                self.package_name,
                            )
                            check_and_prompt.printred(
                                "To upgrade to version ",
                                self.pypi_version,
                                " manually, please use:",
                                italics,
                                " pip install --upgrade ",
                                self.package_name,
                            )
                            check_and_prompt.printred(line, "\n", bold=True)
                            check_and_prompt.write_file(self, "remind")
                        elif prompt_choice == "3":
                            check_and_prompt.printred(
                                "\nVersion ",
                                self.pypi_version,
                                " of ",
                                self.package_name,
                                " will be skipped",
                            )
                            check_and_prompt.printred(
                                "You will be prompted again when the next version of ",
                                self.package_name,
                                " is released",
                            )
                            check_and_prompt.printred(
                                "To upgrade to version ",
                                self.pypi_version,
                                " manually, please use:",
                                italics,
                                " pip install --upgrade ",
                                self.package_name,
                            )
                            check_and_prompt.printred(line, "\n", bold=True)
                            check_and_prompt.write_file(self, "skip")
                        elif prompt_choice == "4":
                            check_and_prompt.printred(
                                "\nYou will never again be prompted to upgrade ",
                                self.package_name,
                                ", even if you upgrade manually.",
                            )
                            check_and_prompt.printred(
                                "To upgrade to version ",
                                self.pypi_version,
                                " manually, please use:",
                                italics,
                                " pip install --upgrade ",
                                self.package_name,
                            )
                            check_and_prompt.printred(line, "\n", bold=True)
                            check_and_prompt.write_file(self, "neveragain")
                            # If users select this option, "neveragain" is written to check4updates.txt in the package's directory.
                            # If they update manually the check4updates.txt file is not deleted so their choice to never be prompted again will remain.
                            # The only way to overwrite this is for the user to manually delete the check4updates.txt file.
            else:
                # make a note in the txt file if there has been another failure to connect.
                # this will be used to increase the online check interval
                check_and_prompt.write_file(
                    self, string="connectionerror", count=self.count + 1
                )

        self.script_duaration = (time.time() - prompt_delay) - start_time
        os.chdir(path=cwd)  # reset the current working directory

    def write_file(self, string, count=1):
        """
        write the check4updates.txt file in the format
        action time version count
        the string arg provided is the action which will be either checked, remind, skip, connectionerror, neveragain
        """
        f = open("check4updates.txt", "w")
        f.write(
            str(
                string
                + " "
                + str(int(time.time()))
                + " "
                + self.pypi_version
                + " "
                + str(count)
                + "\n"
            )
        )  # this will write "remind/skip/checked/connectionerror/neveragain timestamp_of_decision pypi_version_of_decision count"
        f.close()

    def read_file(self):
        """
        read the check4updates.txt file to obtain the values action, time, version, count
        The version here is the pypi version when the file was written
        """
        try:
            f = open("check4updates.txt", "r")
            line = f.readline().strip("\n")
            f.close()
            read_line = line.rsplit(" ")
            read_action, read_time, read_version, read_count = (
                read_line[0],
                read_line[1],
                read_line[2],
                int(read_line[3]),
            )
        except FileNotFoundError:
            read_action, read_time, read_version, read_count = (
                None,
                0,
                "0.0.0",
                0,
            )  # file does not exist
        self.action = read_action
        self.timestamp = read_time
        self.version = read_version
        self.count = read_count

    def get_pypi_version(self):
        """
        webscrape PyPI to obtain the most recent version
        this part takes about 1 second to execute so we only check online if we haven't checked for a while
        when to check is controlled by online_check_interval
        """
        import requests
        import re
        from requests.exceptions import ConnectionError

        index = "https://pypi.python.org/simple"
        url = "{}/{}/".format(index, self.package_name)
        try:
            page = requests.get(url).text
            pattern = r">{}-(.+?)<".format(self.package_name)
            tar_version = re.findall(pattern=pattern, string=page, flags=re.I)[-1]
            pattern2 = r"([0-9]+(\.[0-9]+)+)"
            self.pypi_version = re.findall(
                pattern=pattern2, string=tar_version, flags=re.I
            )[0][0]
        except ConnectionError:
            self.pypi_version = "connectionerror"

    def get_installed_version(self):
        """
        check which version is currently installed in the user's system
        """
        import pkg_resources

        installed_version = pkg_resources.get_distribution(self.package_name).version
        self.installed_version = installed_version

    @staticmethod
    def printred(*args, bold=False):
        """
        Prints in red

        :param args: accepts as many string args as required and DOES NOT separate them by a space
        :param bold: Option to bold the text. Default is False
        """
        arglist = list(args)
        string = "".join(arglist)  # unlike print() there is no space added between args

        if bold is True:
            BOLD = "\033[1m"
        else:
            BOLD = "\033[21m"
        RED = "\033[91m"
        ENDTEXT = "\033[0m"
        print(BOLD + RED + string + ENDTEXT)

    @staticmethod
    def pad_zeros(list_of_strings, padding=5):
        """
        adds preceeding zeros to strings so the length of the total string is equal to the arg padding
        Does this for each item in the list then joins the items are returns the joined item
        eg. ['1234','12','1'] with padding=5 becomes '012340001200001'
        """
        out = ""
        for string in list_of_strings:
            out += "0" * (padding - len(string)) + string
        return out
