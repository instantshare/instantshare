from storage.storage import Storage


class Test(Storage):

    def initialize(self):
        print("initialize() called")
        pass

    def upload(self, file: str) -> str:
        print("upload() called")
        return "It works!"
