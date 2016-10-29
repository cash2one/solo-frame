try:
    import _hash_
    vars().update(vars(_hash_))
except Exception:
    pass
