from collections import MutableMapping
import string
import random


def random_string(l):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(l))


class Game(MutableMapping):
    def __init__(self):
        self.props = {}
        self.props["url"] = random_string(6)
        self.props["secret"] = {}
        self.props["secret"]["one"] = random_string(3)
        self.props["secret"]["two"] = random_string(3)

    def __delitem__(self):
        pass

    def __getitem__(self, key):
        return self.props[key]

    def __iter__(self):
        return iter(self.props)

    def __len__(self):
        return len(self.props)

    def __setitem__(self, item, value):
        self.props[item] = value
