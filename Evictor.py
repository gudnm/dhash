class Evictor(object):
    def __init__(self):
        pass

    def update_on_read(self):
        pass

    def remove_for_write(self):
        pass

class LRU(Evictor):
    """Implement Least-Recently-Used eviction strategy."""
    pass

class LFU(Evictor):
    """Implement Least-Frequently-Used eviction strategy."""
    pass

class FIFO(Evictor):
    """Implement First-In-First-Out eviction strategy."""
    pass
