# -*- coding: utf-8 -*-

"""Executor.

This module executes commands.
"""

import subprocess
from data import data


def execute(command_id):
    """Execute the command related to the command_id.

    This function executes the command it can match with command_id using
    the data module.

    If the command is found then a child process will be started. It does not
    wait for its termination.

    Args:
        command_id: The id which will be matched with a command from the data
            module. This argument will be casted to a string.

    Returns:
        True if the related command was found and it tried to launch it. False
        otherwise.
    """
    command_id = str(command_id)
    command, arguments = data.get_command_and_arguments(command_id)
    if command is None:
        print("ERROR: executor: The command related to the detected symbol "
              "is missing.")
        return False
    else:
        subprocess.Popen([command, arguments])
        return True
