from collections import MutableMapping
import string
import random
import json
import chess


def random_string(l):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(l))


class Game(MutableMapping):
    def __init__(self, props=None):
        if not props:
            self.props = {}
            self.props["_id"] = random_string(6)
            self.props["secret"] = {}
            self.props["secret"]["w"] = random_string(4)
            self.props["secret"]["b"] = random_string(4)
            self.props["fen"] = chess.Board().fen()
        else:
            self.props = json.loads(props)

    def __delitem__(self, key):
        del self.props[key]

    def __getitem__(self, key):
        return self.props[key]

    def __iter__(self):
        return iter(self.props)

    def __len__(self):
        return len(self.props)

    def __setitem__(self, item, value):
        self.props[item] = value

    def get_fen(self):
        return self.props["fen"]

    def legal_moves(self):
        s = chess.Board(self.props["fen"]).legal_moves
        return [x.uci() for x in list(s)]

    def push_san(self, move):
        temp = chess.Board(self.props["fen"])
        temp.push_san(move)
        self.props["fen"] = temp.fen()
