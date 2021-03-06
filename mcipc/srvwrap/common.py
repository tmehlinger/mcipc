"""Common stuff."""

from contextlib import suppress
from threading import Thread


__all__ = ['Daemon']


class Daemon:
    """An abstract daemon."""

    def __init__(self):
        """Sets host and port."""
        self._thread = None
        self._terminate = False

    def __enter__(self):
        """Starts the daemon."""
        self.start()
        return self

    def __exit__(self, *_):
        """Stops the daemon."""
        self.stop()

    @property
    def status(self):
        """Returns True iff the daemon is running else False."""
        return self._thread is not None

    def _run(self):
        """Runs the ZMQ server."""
        raise NotImplementedError()

    def start(self):
        """Starts the server."""
        if not self.status:
            self._terminate = False
            self._thread = Thread(target=self._run)
            self._thread.start()
            return True

        return False

    def stop(self):
        """Stops the server."""
        self._terminate = True

        with suppress(AttributeError):
            self._thread.join()
