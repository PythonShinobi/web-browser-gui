import os

class Paths:
    base = os.path.dirname(__file__)
    icons = os.path.join(base, 'assets')

    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icons, filename)