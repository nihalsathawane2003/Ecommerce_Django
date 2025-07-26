# utils/cache.py
from django.core.cache import cache

def cache_set(key, value, timeout=60 * 15):  # Default 15 minutes
    cache.set(key, value, timeout)

def cache_get(key):
    return cache.get(key)

def cache_delete(key):
    cache.delete(key)
