# -*- coding: utf-8 -*-

import subprocess
from data import data

def execute(command_id):
    command_id = str(command_id)
    command, arguments = data.get_command_and_arguments(command_id)
    subprocess.Popen([command, arguments])
