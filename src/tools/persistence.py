import logging
import os
import pickle

import tools.encryption as crypt
from tools import dirs

persistent_data_dir = dirs.data


class PersistentDataEncryptedError(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class KVStore(dict):
    """
    An extended dictionary that is similar to Python's "shelve", but optionally
    supports encryption. Also supports transitions between encrypted and
    unencrypted modes.
    """

    def __init__(self, module_name=".general", pw=None, unlock=False):
        """
        Initialize a KVStore instance. Supply a password to encrypt the data
        on disk. If you set unlock to True, you can decrypt previously
        encrypted data.

        :param module_name:
        Determines which dictionary to use. Will look for a file with that name
        in the persistent data directory.

        :param pw:
        Password for decrypting or encrypting the persistent data. If None,
        will not encrypt the data on disk. Has to be specified for decryption
        when unlock == True.

        :param unlock:
        If True, will decrypt existing persistent data using specified pw and
        write unencrypted data back to disk immediately.

        :raises ValueError:
        When unlock is set to True, but no password is supplied. The password
        is needed for decryption.

        :raises crypt.CryptoError:
        When the supplied password is wrong.

        :raises PersistentDataEncryptedError:
        When encryption was turned off by the user since the last run and the
        data is still encrypted. In this case, you should specify a pw and set
        unlock to True. This will decrypt the data on disk.
        """

        if unlock and not pw:
            raise ValueError("you have to supply a password to unlock the stored data")

        super().__init__()
        self._filepath = os.path.join(persistent_data_dir, module_name)
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
                # load and sync back if clear
                # raise crypt.CryptoError again when password was wrong
                try:
                    self.update(pickle.loads(binary_data))
                except:
                    raise crypt.CryptoError
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


class KVStub(KVStore):

    def __init__(self, *args, **kwargs):
        # don't actually do anything
        pass

    def __getattr__(self, item):
        # overwrite any calls to this object
        raise NotImplementedError
