"""Defining the progress result handler."""
# pylint: disable=too-many-arguments
from __future__ import absolute_import, print_function

import os
import sys
import threading

from rotest.core import skip_if_flow
from rotest.core.result.handlers.abstract_handler import AbstractResultHandler

from .utils import (wrap_settrace, go_over_tests, create_current_bar,
                    DummyFile, StatisticManager)


class CurrentProgressHandler(AbstractResultHandler):
    """CurrentProgressHandler interface.

    Attributes:
        stream (file): stdout file to write to.
    """
    NAME = 'progress'
    watcher_thread = None

    def __init__(self, *args, **kwargs):
        super(CurrentProgressHandler, self).__init__(*args, **kwargs)
        self.stream = kwargs['stream']
        if hasattr(self.stream, 'stream'):
            # In case it's a container of an inner stream
            self.stream.stream = DummyFile(self.stream.stream)

        else:
            sys.stdout = DummyFile(self.stream)

    def start_test_run(self):
        """Called once before any tests are executed."""
        wrap_settrace()
        StatisticManager.calculate_expected_time(self.main_Test)

    def stop_test_run(self):
        """Called once after all tests are executed."""
        if self.watcher_thread:
            self.watcher_thread.join()

        print(os.linesep)

    @skip_if_flow
    def start_test(self, test):
        """Called when the given test is about to be run."""
        test.progress_bar = create_current_bar(test)
        test.progress_bar.start = True
        self.watcher_thread = threading.Thread(target=go_over_tests,
                                               kwargs={"test": test,
                                                       "use_color": False})
        self.watcher_thread.setDaemon(True)
        self.watcher_thread.start()

    def stop_test(self, test):
        """Called when the given test has been run.

        Args:
            test (rotest.core.abstract_test.AbstractTest): test item instance.
        """
        if hasattr(test, 'progress_bar'):
            test.progress_bar.finish = True
            if self.watcher_thread:
                self.watcher_thread.join()
                self.watcher_thread = None
