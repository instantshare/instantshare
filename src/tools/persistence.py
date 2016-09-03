import logging
import pickle
import os

import tools.encryption as crypt


persistent_data_dir = "data/"


class KVStore(dict):

    def __init__(self, module_name="general", pw=None):
        super().__init__()
        # TODO: this is user data - put this where it belongs
        os.makedirs(persistent_data_dir, exist_ok=True)
        self._filepath = persistent_data_dir + module_name
        self._encrypted = pw is not None

        if self._encrypted:
            self._key = crypt.SymmetricKey(pw)

        # try to load persistent data
        data = {}
        dirty = False

        # data read by pickle has to be a dict, just to make sure
        def validate(x):
            if not isinstance(x, dict):
                raise TypeError("The data read from disk has to be a dict.")
            return x

        try:
            with open(self._filepath, mode="rb") as file:
                binary_data = file.read()

            if self._encrypted:
                try:
                    # decrypt binary data and deserialize
                    data = validate(pickle.loads(self._key.decrypt(binary_data)))
                except crypt.CryptoError:
                    # data was not encrypted yet
                    data = pickle.loads(binary_data)
                    dirty = True
            else:
                # deserialize binary data
                try:
                    data = pickle.loads(binary_data)
                except:
                    # except is intentionally broad: pickle throws a variety of exceptions.
                    # Data was probably encrypted, if not, we will catch the error later again.
                    # TODO ask user for password instead of overwriting data
                    logging.error("Trying to load encrypted data without decryption key.")
                    dirty = True
        except:
            # except is intentionally broad:
            # If anything happens, we can only overwrite the old data.
            # There is no data yet, or the data has been corrupted.
            pass
        else:
            self.update(data)
            if dirty:
                self.sync()

    def sync(self):
        data = {}
        data.update(self)
        bdata = pickle.dumps(data)
        with open(self._filepath, mode="wb") as file:
            if self._encrypted:
                file.write(self._key.encrypt(bdata))
            else:
                file.write(bdata)
