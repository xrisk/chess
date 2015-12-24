from collections import MutableMapping
import string
import random
import chess


def random_string(l):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(l))


class Game(MutableMapping):
    def __init__(self):
        self.props = {}
        self.props["url"] = random_string(6)
        self.props["secret"] = {}
        self.props["secret"]["white"] = random_string(3)
        self.props["secret"]["black"] = random_string(3)
        self.props["fen"] = chess.Board().fen()

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

    def get_fen(self):
        return self.props["fen"]

    def moves_here(self):
        s = chess.Board(self.props["fen"]).legal_moves
        return [x.uci() for x in list(s)]

    def move_white(self, move, secret):
        if self.props["secret"]["white"] == secret:
            if move in self.moves_here():
                temp = chess.Board(self.props["fen"])
                temp.push_uci(move)
                self.props["fen"] = temp.fen()
                return self.props["fen"]

    def move_black(self, move, secret):
        if self.props["secret"]["black"] == secret:
            if move in self.moves_here():
                temp = chess.Board(self.props["fen"])
                temp.push_sa(move)
                self.props["fen"] = temp.fen()
                return self.props["fen"]
