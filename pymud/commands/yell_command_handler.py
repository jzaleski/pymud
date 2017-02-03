from .base_command_handler import BaseCommandHandler


class YellCommandHandler(BaseCommandHandler):
    def __init__(self):
        BaseCommandHandler.__init__(
            self,
            'yell',
            2
        )

    def range_0(self, source, args):
        return 'You belt out, "%s"' % ' '.join(args)

    def range_1(self, source, args):
        return '%s yells, "%s"' % (
            source.character.name,
            ' '.join(args),
        )

    def range_2(self, source, args):
        return self.range_1(
            source,
            args
        )
