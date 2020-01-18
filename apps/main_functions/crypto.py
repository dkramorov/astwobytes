# -*- coding: utf-8 -*-
import hashlib

def serp_hash(text):
    """Хэш строки"""
    m = hashlib.sha256()
    m.update(text)
    return m.hexdigest()

