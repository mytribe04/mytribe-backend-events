"""
Utilities / interfaces related to cryptography
"""

import abc
import hashlib


class KeyManager(abc.ABC):
    """
    Abstract base class for a cryptographic key manager. At the time of initialization, it will acquire access to
    a key. Has methods to encrypt and decrypt data passed to it (using the previously initialized key)
    """

    @property
    def name(self) -> str:
        """ Returns the name of the concrete class of the instantiated KeyManager object """
        return self.__class__.__name__

    @abc.abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        """
        Encrypt `plaintext` and return the encrypted version
        """

    @abc.abstractmethod
    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Encrypt `encrypted_data` and return the plaintext version
        """


class MockKeyManager(KeyManager):
    """
    Mock key manager that simply encodes/decodes data but does not encrypt it.

    DO NOT USE IN PRODUCTION !
    """

    def __init__(self, encoding='utf-8'):
        self._encoding = encoding

    def encrypt(self, plaintext: str) -> bytes:
        if plaintext is None:
            return None
        return plaintext.encode(self._encoding)

    def decrypt(self, encrypted_data: bytes) -> str:
        if encrypted_data is None:
            return None
        return encrypted_data.decode(self._encoding)


class DjangoCachingProxyKeyManager(KeyManager):
    """
    Key manager that simply acts as a proxy for an actual KeyManager implementation,
    but caches decrypted values using a Django cache
    """

    def __init__(self, key_manager: KeyManager, cache, cache_ttl: int = 3600, cache_prefix: str = None):
        if not key_manager or not isinstance(key_manager, KeyManager):
            raise TypeError("key_manager (instance of KeyManager) is mandatory")

        if not cache:
            raise ValueError("cache is required")

        if not isinstance(cache_ttl, (int, float)) or cache_ttl <= 0:
            raise ValueError("ttl is required")

        self._key_manager = key_manager
        self._cache = cache
        self._cache_prefix = cache_prefix
        self._cache_ttl = cache_ttl

    def encrypt(self, plaintext: str) -> bytes:
        return self._key_manager.encrypt(plaintext)

    def decrypt(self, encrypted_data: bytes) -> str:
        cache_key = hashlib.sha256(encrypted_data).hexdigest()
        plaintext = self._cache.get(cache_key, None)

        if not plaintext:
            plaintext = self._key_manager.decrypt(encrypted_data)
            if plaintext:
                self._cache.set(cache_key, plaintext, self._cache_ttl)

        return plaintext
