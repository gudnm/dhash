class Evictor(object):
    def __init__(self):
        pass

    def get_evictions(self):
        pass

class LRU(Evictor):
    """Implement Least-Recently-Used eviction strategy."""
    pass

class LFU(Evictor):
    """Implement Least-Frequently-Used eviction strategy."""
    pass

class FIFO(Evictor):
    """Implement First-In-First-Out eviction strategy."""
    def __init__(self):
        pass
    def get_evictions(self, node, key):
        evictions = []
        
        return evictions
