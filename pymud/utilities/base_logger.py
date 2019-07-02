import datetime
import traceback


class BaseLogger(object):
    def __init__(self, output_stream):
        self._output_stream = output_stream
        self._log_debug = True
        self._log_error = True
        self._log_info = True
        self._log_warn = True

    def debug(
        self,
        message,
        stack_trace=None
    ):
        if self._log_debug:
            self._write(
                'DEBUG',
                message,
                stack_trace
            )

    def error(
        self,
        message,
        stack_trace=None
    ):
        if self._log_error:
            self._write(
                'ERROR',
                message,
                stack_trace
            )

    def info(
        self,
        message,
        stack_trace=None
    ):
        if self._log_info:
            self._write(
                'INFO',
                message,
                stack_trace
            )

    def warn(
        self,
        message,
        stack_trace=None
    ):
        if self._log_warn:
            self._write(
                'WARN',
                message,
                stack_trace
            )

    def _write(
        self,
        level,
        message,
        stack_trace
    ):
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
            traceback.print_tb(stack_trace, file=self._output_stream)
