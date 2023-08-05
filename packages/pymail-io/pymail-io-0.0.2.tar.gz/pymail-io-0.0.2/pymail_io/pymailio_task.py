from typing import Dict, Any

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO


class PyMailIOTask(AbstractPyMailIO, PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailIOTask, self).__init__(self, *args, **kwargs)

    def send_email(self, *, subject, body) -> Any:
        """
        :param subject:
        :param body:
        :return:
        """
        self.pytask.run()
        metadata = self.send_email_on_queue(subject, body)
        self.pytask.stop()
        return metadata

    def get_task(self, metadata):
        """
        :param metadata:
        :return:
        """
        return self.pytask.get_task(metadata)
