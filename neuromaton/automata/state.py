"""Module for describing state constructs."""


class State(object):
    """A state within our DFA. Needs to be hashable."""

    __slots__ = ('accepting')

    def __init__(self, accepting: bool = False):
        self.accepting = accepting
