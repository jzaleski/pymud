from .base_command_handler import BaseCommandHandler


class SayCommandHandler(BaseCommandHandler):
    def __init__(self):
        super(SayCommandHandler, self).__init__('say', 1)

    def range_0(
        self,
        source,
        args
    ):
        return 'You say, "%s"' % ' '.join(args)

    def range_1(
        self,
        source,
        args
    ):
        return '%s says, "%s"' % (source.character.name, ' '.join(args))
