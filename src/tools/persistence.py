import logging
import pickle

from tools.encryption import SymmetricKey


class KVStore(dict):

    def __init__(self, module_name="general", pw=None):
        super().__init__()
        self._filepath = "data/" + module_name
        self._encrypted = pw is not None

        if self._encrypted:
            self._key = SymmetricKey(pw)

        # try to load persistent data
        data = None

        # data read by pickle has to be a dict
        def validate(x):
            if not isinstance(x, dict):
                raise pickle.UnpicklingError
            return x

        try:
            with open(self._filepath, mode="rb") as file:
                binary_data = file.read()

            if self._encrypted:
                try:
                    # decrypt binary data and deserialize
                    data = validate(pickle.loads(self._key.decrypt(binary_data)))
                except pickle.UnpicklingError:
                    # data was not encrypted yet
                    data = pickle.loads(binary_data)
            else:
                try:
                    # deserialize binary data
                    data = validate(pickle.loads(binary_data))
                except pickle.UnpicklingError:
                    # data was encrypted before
                    # TODO ask user for encryption key?
                    logging.error("Trying to load encrypted data without decryption key.")

        except IOError:
            # there is no persistent data yet, which is okay
            pass
        else:
            self.update(data)

    def sync(self):
        data = {}
        data.update(self)
        bytes = pickle.dumps(data)
        with open(self._filepath, mode="wb") as file:
            if self._encrypted:
                file.write(self._key.encrypt(bytes))
            else:
                file.write(bytes)
