import datetime, traceback


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
        traceback=None
    ):
        if self._log_debug:
            self._write(
                'DEBUG',
                message,
                traceback
            )

    def error(
        self,
        message,
        traceback=None
    ):
        if self._log_error:
            self._write(
                'ERROR',
                message,
                traceback
            )

    def info(
        self,
        message,
        traceback=None
    ):
        if self._log_info:
            self._write(
                'INFO',
                message,
                traceback
            )

    def warn(
        self,
        message,
        traceback=None
    ):
        if self._log_warn:
            self._write(
                'WARN',
                message,
                traceback
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
