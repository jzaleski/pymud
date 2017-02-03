import datetime, sys, traceback


class BaseLogger(object):
    def __init__(self, output_stream):
        self.__output_stream = output_stream

    @property
    def _log_debug(self):
        return True

    @property
    def _log_error(self):
        return True

    @property
    def _log_info(self):
        return True

    @property
    def _output_stream(self):
        return self.__output_stream

    def debug(self, message, traceback=None):
        if self._log_debug:
            self.__write(
                'DEBUG',
                message,
                traceback
            )

    def error(self, message, traceback=None):
        if self._log_error:
            self.__write(
                'ERROR',
                message,
                traceback
            )

    def info(self, message, traceback=None):
        if self._log_info:
            self.__write(
                'INFO',
                message,
                traceback
            )

    def __write(self, level, message, stack_trace):
        now = datetime.datetime.now()
        self._output_stream.write(
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
                file=self._output_stream
            )
