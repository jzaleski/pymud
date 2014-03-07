from .base_logger import BaseLogger

from .console_output_stream import ConsoleOutputStream

class ConsoleLogger(BaseLogger):

    def __init__(self):
        BaseLogger.__init__(self)
        self.__output_stream = ConsoleOutputStream()

    def _get_output_stream(self):
        return self.__output_stream
