from abc import ABCMeta, abstractmethod


class Storage(metaclass=ABCMeta):
    """
    Abstract Base Class for Cloud Storage Providers
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize the storage (authentication and authorization)
        """

    @abstractmethod
    def upload(self, file: str) -> str:
        """
        Upload the specified file to the storage
        :param file: full path to file
        :return: URL of uploaded file
        """