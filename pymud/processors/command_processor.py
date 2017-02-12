import sys

from os.path import (
    dirname,
    getmtime,
    join as join_path,
)

from pymud import LOGGER

from .base_processor import BaseProcessor


class CommandProcessor(BaseProcessor):
    def __init__(self, client_connection):
        BaseProcessor.__init__(
            self,
            client_connection
        )
        self.__exit_commands = [
            'exit',
            'quit',
        ]

    def process(self):
        command = self._client_connection.recv(256) or ''
        if not command:
            return True
        LOGGER.debug(
            '%s:%s - %s [fromclient]' % (
                self._client_connection.remote_ip,
                self._client_connection.remote_port,
                command,
            )
        )
        if command[0:1] == "'":
            command = 'say ' + command[1:]
        LOGGER.debug(
            '%s:%s - %s [translated]' % (
                self._client_connection.remote_ip,
                self._client_connection.remote_port,
                command,
            )
        )
        args = command.split(' ')
        args0_lc = args[0].lower()
        if args0_lc in self.__exit_commands:
            LOGGER.debug(
                '%s:%s - %s disconnected' % (
                    self._client_connection.remote_ip,
                    self._client_connection.remote_port,
                    self._client_connection.character.name,
                )
            )
            return False
        command_handler = self.__get_command_handler(args0_lc)
        if not command_handler:
            self._client_connection.send(
                'I could not find what you were referring to'
            )
        else:
            command_handler.handle(
                self._client_connection,
                args[1:]
            )
        return True

    def __get_command_handler(self, command):
        module_name, class_name = \
            self.__get_module_name_and_class_name_for_command(command)
        self.__import_command_handler(module_name)
        return self.__instantiate_command_handler(module_name, class_name)

    def __get_module_name_and_class_name_for_command(self, command):
        return (
            'pymud.commands.%s_command_handler' % command.lower(),
            '%sCommandHandler' % command.capitalize(),
        )

    def __has_source_file_changed(self, module_name):
        source_file_name, compiled_file_name = [
            join_path(
                dirname(sys.modules[module_name].__file__),
                module_name.split('.')[-1] + extension,
            ) for extension in ('.py', '.pyc')
        ]
        return getmtime(source_file_name) > getmtime(compiled_file_name)

    def __import_command_handler(self, module_name):
        if module_name in sys.modules:
            if self.__has_source_file_changed(module_name):
                LOGGER.debug('reloading module: "%s"' % module_name)
                reload(sys.modules[module_name])
                LOGGER.debug('reloaded module: "%s"' % module_name)
        else:
            try:
                LOGGER.debug('importing module: "%s"' % module_name)
                __import__(module_name)
                LOGGER.debug('imported module: "%s"' % module_name)
            except ImportError:
                LOGGER.error('module: "%s" does not exist' % module_name)

    def __instantiate_command_handler(self, module_name, class_name):
        return None if module_name not in sys.modules else getattr(
            sys.modules[module_name],
            class_name,
            lambda: None
        )()
