from abc import ABCMeta, abstractmethod

__all__ = ["dropbox", "googledrive", "storage_providers"]

storage_providers = {}


def register(clazz):
    storage_providers[clazz.name()] = clazz
    return clazz


class Base(metaclass=ABCMeta):
    """
    Abstract Base Class for Cloud Storage Providers
    """

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

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        :return: The Storage Provider identifier string, such as "googledrive" for Google Drive
        """
        pass

