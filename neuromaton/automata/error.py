"""Module for errors"""


class Error(Exception):
    """Base error class for this module."""


class InvalidStartingState(Error):
    """Invalid starting state."""

    def __init__(self, state):
        """Denote the invalid starting state."""
        super().__init__('%s is not a valid starting state.' % state)


class InvalidAcceptingStates(Error):
    """For when one or more of the accepting states is bad."""

    def __init__(self, states):
        """Denote the invalid accepting states."""
        super().__init__('One or more invalid accepting states: %s' % states)


class IllegalTransition(Error):
    """Raised when a transition doesn't work."""

    def __init__(self, start, symbol):
        """Incorporate attempted start + transition."""
        super().__init__(
            'Illegal transition %s from starting node %s' % start, symbol)
