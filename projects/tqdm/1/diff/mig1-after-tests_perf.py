#mig=skip

from __future__ import print_function, division
from contextlib import contextmanager
from functools import wraps
from time import sleep, time
# Use relative/cpu timer to have reliable timings when there is a sudden load
try:
    from time import process_time
except ImportError:
    from time import clock
    process_time = clock
import sys

from tqdm import tqdm, trange
from tests_tqdm import pretest_posttest  # NOQA
from tests_tqdm import skip, StringIO, closing, _range, patch_lock


def cpu_sleep(t):
    """Sleep the given amount of cpu time"""
    start = process_time()
    while (process_time() - start) < t:
        pass


def checkCpuTime(sleeptime=0.2):
    """Check if cpu time works correctly"""
    if checkCpuTime.passed:
        return True
    # First test that sleeping does not consume cputime
    start1 = process_time()
    sleep(sleeptime)
    t1 = process_time() - start1

    # secondly check by comparing to cpusleep (where we actually do something)
    start2 = process_time()
    cpu_sleep(sleeptime)
    t2 = process_time() - start2

    if abs(t1) < 0.0001 and t1 < t2 / 10:
        checkCpuTime.passed = True
        return True
    skip("cpu time not reliable on this machine")