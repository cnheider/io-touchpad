# -*- coding: utf-8 -*-

class Command(object):

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments

    def get_command_and_argument(self):
        return self.command, self.arguments

    @staticmethod
    def is_user_defined(command_id):
        return command_id in _USER_DEFINED_COMMANDS

    @staticmethod
    def is_builtin(command_id):
        return command_id in _BUILTIN_COMMANDS

_USER_DEFINED_COMMANDS = {}
_BUILTIN_COMMANDS = {
    '1': Command('gedit', ''),
}


def get_command_and_arguments(command_id):
    if Command.is_builtin(command_id):
        return _BUILTIN_COMMANDS[command_id].get_command_and_argument()
    elif Command.is_user_defined(command_id):
        return _USER_DEFINED_COMMANDS[command_id].get_command_and_argument()


