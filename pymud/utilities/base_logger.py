import datetime, sys, traceback

class BaseLogger(object):

    def __init__(self):
        self.__log_debug = True
        self.__log_error = True
        self.__log_info = True

    def debug(self, message, traceback=None):
        if self.__log_debug:
            self.__write(
                'DEBUG',
                message,
                traceback
            )

    def error(self, message, traceback=None):
        if self.__log_error:
            self.__write(
                'ERROR',
                message,
                traceback
            )

    def info(self, message, traceback=None):
        if self.__log_info:
            self.__write(
                'INFO',
                message,
                traceback
            )

    def _get_output_stream(self):
        raise NotImplementedError()

    def __write(self, level, message, stack_trace):
        now = datetime.datetime.now()
        output_stream = self._get_output_stream()
        output_stream.write(
            '%s %s [%s]: %s\n' % (
                str(now.date()),
                now.time().strftime('%H:%M:%S'),
                level,
                message,
            )
        )
        if stack_trace:
            traceback.print_tb(
                stack_trace,
                file=output_stream
            )
