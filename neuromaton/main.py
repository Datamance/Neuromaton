"""The neuromaton class file."""
from automata import DeterministicFiniteAutomaton


class Neuromaton(DeterministicFiniteAutomaton):
    """The NDFA that will carry out our calculations."""


class Neuron(object):
    """A neuron. We just want to see if this is hashable."""
    pass


if __name__ == '__main__':

    neuromaton = Neuromaton()
