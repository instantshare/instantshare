from storage.storage import Storage
import logging

class Test(Storage):

    def initialize(self):
        logging.info("Test initialize was called")
        pass

    def upload(self, file: str) -> str:
        logging.info("Test upload was called")
        return file
