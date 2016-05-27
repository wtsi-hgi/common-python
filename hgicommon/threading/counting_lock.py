from threading import Lock


class _CountingLock(object):
    """ Lock that keeps count of threads waiting to acquire itself """
    def __init__(self, *args, **kwargs):
        """ Wraps Lock constructor """
        self._lock = Lock(*args, **kwargs)

        self._wait_lock = Lock()
        self._waiting = 0

    def acquire(self, *args, **kwargs):
        """ Wraps Lock.acquire """
        with self._wait_lock:
            self._waiting += 1

        self._lock.acquire(*args, **kwargs)

        with self._wait_lock:
            self._waiting -= 1

    def release(self):
        """ Wraps Lock.release """
        self._lock.release()

    def waiting_to_acquire(self) -> int:
        """ Return the number of threads waiting to acquire the lock """
        with self._wait_lock:
            waiting = self._waiting
        return waiting

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
