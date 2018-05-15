"""Finite Automata module.

It works very simply:

The transition function will have symbols. These symbols transition between
States. States are nodes in our *FAs.

The most basic transition mapping is just a sequence like so:
start and end nodes:

- (
    ('enter_coin', ('locked', 'unlocked'), {}),
    ('push_turnstile', ('unlocked', 'locked'), {})
  )
or


This mapping is required.

Sometimes, however, we want to have more complicated transition functions -
perhaps even ones that evolve with time. This means adding some flexibility to
the mapping mechanism.

As such, there are two options for adding more powerful state transitions:

1) Use functions as keys in new_transitions. The constructor will attach the
   function to the TF class and make a token for it based on the name. Note
   that these functions need to be structured *exactly* like the instance
   methods you'd normally define on a class, *and* the argument signature for
   each must include the nodes you've specified in the mapping.

2) Subclass FiniteAutomata with instance methods that correspond
   to the tokens you want custom behavior for.

A third will be added soon - Scheme expressions.


"""
from typing import Sequence, Hashable, Dict
import functools
import networkx
import matplotlib.pyplot as plt

TRANSITION = '__TRANSITION_FUNCTION'


class FiniteAutomaton(networkx.MultiDiGraph):
    """The transition function class."""

    def __init__(self, new_transitions: Sequence, initial_state: Hashable,
                 **kwargs):
        """Constructor."""
        super().__init__(**kwargs)  # loads kwargs to graph property

        self.current = initial_state

        for transition in new_transitions:
            if len(transition) == 2:
                symbol, states = transition
                self.add_transition(symbol, states)
            elif len(transition) == 3:
                symbol, states, attr_dict = transition
                self.add_transition(symbol, states, attr_dict)

    def __call__(self, symbol: Hashable, **kwargs):
        """The callable aspect of the transition function.

        The use of varargs here adds a new element not typically seen in FAs -
        basically, externally-mediated effects on the transition itself.
        """
        targets = self.adj[self.current]

        if targets:
            for target_state, transitions in targets.items():
                # target state is a string
                if symbol in transitions:
                    targets[target_state][symbol][TRANSITION](**kwargs)
        else:
            print('Failure to transition: no available connection!')

    def _default(self, current_state: Hashable, next_state: Hashable, **attrs):
        """Default transition."""
        print(f'moving from {current_state} to {next_state}')
        print('attributes: ', attrs)
        self.current = next_state

    def add_transition(
            self, symbol: Hashable, states: Sequence[Hashable],
            attrs: Dict = None):
        """Adds a transition type between a token and two states.

        Here, attrs should be things about the transition _in general_ that we
        may override on individual transitions!
        """
        attrs = attrs or {}
        # Note - we could do first_state, *next_states = states. This would
        # allow us to construct multiple targets pretty easily, though we
        # should probably allow a Sequence of Sequences first (explicitly
        # denoting the relationship between origin and destination nodes).
        first_state, next_state = states

        if callable(symbol):  # could do type(symbol) == type(lambda: None)
            symbol_name = symbol.__name__

            setattr(self, symbol_name, symbol)

            # This will add nodes if they're not already in the graph.
            self.add_edge(first_state, next_state, key=symbol_name, **attrs)

            self[first_state][next_state][symbol_name][TRANSITION] = (
                functools.partial(
                    getattr(self, symbol_name), self, first_state, next_state))

        else:
            self.add_edge(first_state, next_state, key=symbol, **attrs)

            transition = getattr(self, symbol, None)

            if transition:
                self[first_state][next_state][symbol][TRANSITION] = (
                    functools.partial(transition, first_state, next_state))
            else:
                self[first_state][next_state][symbol][TRANSITION] = (
                    functools.partial(self._default, first_state, next_state))


def test():
    transitions = (
        ('enter_coin', ('locked', 'unlocked')),
        ('push', ('unlocked', 'locked'), {})
    )

    class Turnstile(FiniteAutomaton):
        """Test class."""

        def enter_coin(self, first, second, **kwargs):
            if kwargs.pop('coin_value', None) == 0.25:
                print('Thanks for entering a quarter!')
                self.current = second
            else:
                print('This turnstile only takes quarters!')

    return Turnstile(transitions, 'locked')


if __name__ == '__main__':

    turnstile = test()
    turnstile('enter_coin')
    turnstile('enter_coin', coin_value=0.25)
    turnstile('push')

    def slam(self, current_state, next_state, **kwargs):
        print('BANG! You slammed it, and it\'s broken.')
        self.current = next_state

    def fix(self, current_state, next_state):
        if current_state is 'broken':
            self.current = next_state
        else:
            print('why fix it if it ain\'t broke?')

    turnstile.add_transition(slam, ('locked', 'broken'), {})
    turnstile.add_transition(fix, ('broken', 'locked'), {})
    turnstile('slam')
    turnstile('push')
    turnstile('fix')
    turnstile('enter_coin', coin_value=0.25)
    turnstile('push')
    plt.subplot(111)
    networkx.draw_circular(turnstile, with_labels=True, font_weight='bold')
    from pprint import pprint
    pprint([k for k in turnstile.edges(data=True)])
    # networkx.draw_networkx_edge_labels(turnstile)
    plt.show()
