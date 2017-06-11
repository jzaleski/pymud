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
        return "[%s]\n%s\nObvious exits: %s" % (
            location.name,
            location.description,
            ', '.join(exit.name for exit in location.exits) if location.exits else 'None',
        )
