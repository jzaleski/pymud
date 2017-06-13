from pymud.network import ClientConnectionManager

from .base_command_handler import BaseCommandHandler


class LookCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(LookCommandHandler, self).__init__('look')

    def range_0(
        self,
        source,
        args
    ):
        location = source.character.location
        return "[%s]\n%s\nAlso here: %s\nObvious exits: %s" % (
            location.name,
            location.description,
            self._get_also_here(source, location),
            self._get_exits(location),
        )

    def _get_also_here(
        self,
        source,
        location
    ):
        return ', '.join(
            self._get_character_description(client_connection.character)
            for client_connection in ClientConnectionManager.instance.get_by_location_except(
                location, [source])
        ) or 'None'

    def _get_character_description(self, character):
        return '%s%s' % (character.name,
            '' if character.state == 'standing' else ' (%s)' % character.state)

    def _get_exits(self, location):
        return ', '.join(exit.name for exit in location.exits) or 'None'
