"""
Copyright 2019, CCL (SOLUTIONS) Group Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import datetime

DATE_FMT = "%Y-%m-%d %H:%M:%S"

__version__ = "0.2.1"
__description__ = "Module to further simplify log generation"
__contact__ = "Alex Caithness"

class Log:
    def __init__(self,
                 out_path:str, *,
                 append=False,
                 delimiter="\t",
                 debug=True,
                 show_caller=False):
        """
        Create a new log

        out_path: output path for the log file
        append: if True, append output to the file in out_path, otherwise overwrite the file
            (default: False)
        delimiter: the delimiter between fields  in output (default: '\t')
        debug: if the log is in debug mode (default: True)
        show_caller: if True, the name of the caller will be appended to the output (default: False)
        """

        self._f = open(out_path, "t" + "a" if append else "w", encoding="utf-8")
        self._delimiter = delimiter
        self._debug = debug
        self._show_caller = show_caller
        self._closed = False
        self._distinct_strings = set()

    def __call__(self, *args, debug_only=False, to_stdout=True, distinct=False, **kwargs):
        """
        Log a message

        args: the message(s) to be written
        debug_only: if True, only print if the log is in debug mode (default: False)
        to_stdout: if True also print to stdout (default: True)
        distinct: if True only print this exact message once
        """
        
        if self._closed:
            raise ValueError("Log is closed")

        if (not debug_only or self._debug) and (not distinct or tuple(args) not in self._distinct_strings):
            if distinct:
                self._distinct_strings.add(tuple(args))

            parts = []

            if self._show_caller:
                caller_name = sys._getframe(1).f_code.co_name
                parts.append(caller_name)

            timestamp = datetime.datetime.now().strftime(DATE_FMT)
            parts.append(timestamp)
            parts.extend(args)
            line = self._delimiter.join(map(str, parts))

            if to_stdout:
                print(line.encode(sys.stdout.encoding, "replace").decode(sys.stdout.encoding))
            self._f.write(line + "\n")

    def close(self):
        """Close the log"""
        self._f.close()
        self._closed = True


def create_unique_log_name(file_name):
    return "{0} {1}.log".format(file_name, datetime.datetime.now().strftime("%d-%m-%Y %H.%M.%S"))