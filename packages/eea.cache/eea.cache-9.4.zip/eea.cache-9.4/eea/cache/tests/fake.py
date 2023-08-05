""" Fake
"""
from zope.interface import implementer
from eea.cache.utility import MemcachedClient
from eea.cache.interfaces import IMemcachedClient


@implementer(IMemcachedClient)
class FakeMemcachedClient(MemcachedClient):
    """ Fake Memcached Client
    """
    _cache = {}

    def invalidate(self, key=None, ns=None, raw=False, dependencies=None):
        """ Invalidate
        """
        for d_key, value in self._cache.items():
            if dependencies == value.get('dependencies'):
                del self._cache[d_key]
                return

    def query(self, key, default=None, ns=None, raw=False):
        """ Query
        """
        if key in list(self._cache.keys()):
            return self._cache[key]['data']
        raise KeyError(key)

    def set(self, data, key, lifetime=None, ns=None,
            raw=False, dependencies=None):
        """ Set
        """
        if not dependencies:
            dependencies = []
        self._cache[key] = {
            'data': data,
            'dependencies': dependencies
        }
