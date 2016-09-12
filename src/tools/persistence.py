import logging
import pickle
import os

import tools.encryption as crypt


persistent_data_dir = "data/"


class PersistentDataEncryptedError(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class KVStore(dict):

    def __init__(self, module_name=".general", pw=None, unlock=False):

        if unlock and not pw:
            raise ValueError("you have to supply a password to unlock the stored data")

        super().__init__()

        # TODO: this is user data - put this where it belongs
        os.makedirs(persistent_data_dir, exist_ok=True)
        self._filepath = persistent_data_dir + module_name
        self._encrypt_on_write = pw is not None and unlock is False
        self._key = crypt.SymmetricKey(pw) if pw else None

        # try to load persistent data
        try:
            with open(self._filepath, mode="rb") as file:
                binary_data = file.read()
        except IOError:
            # there was no usable data, which is okay
            return

        # there is data, load into dict
        if pw:
            try:
                # decrypt, deserialize, update self
                self.update(pickle.loads(self._key.decrypt(binary_data)))
                # sync if the data is to be unlocked
                if unlock:
                    self.sync()
            except crypt.CryptoError:
                # data was not encrypted yet, load and sync back
                self.update(pickle.loads(binary_data))
                self.sync()
        else:
            try:
                # deserialize, update self
                self.update(pickle.loads(binary_data))
            except:
                # intentionally broad: pickle throws a variety of exceptions.
                # data was probably encrypted, let caller handle this
                raise PersistentDataEncryptedError

    def sync(self):
        data = {}
        data.update(self)
        bdata = pickle.dumps(data)
        with open(self._filepath, mode="wb") as file:
            if self._encrypt_on_write:
                file.write(self._key.encrypt(bdata))
            else:
                file.write(bdata)
