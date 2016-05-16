﻿from listeners.tick import Delay
from players.entity import Player as SourcePythonPlayer
from players.helpers import index_from_userid

__all__ = (
    'Player',
)


class Player(SourcePythonPlayer):
    """A player entity class with additional functionality.

    Takes full advantage of the `Effect` class, and implements
    some other missing functionality from Source.Python's player class.
    """

    @classmethod
    def from_userid(cls, userid):
        """Get a player instance directly from an userid."""
        return cls(index_from_userid(userid))

    @property
    def cs_team(self):
        """Get the player's Counter-Strike team as a string.

        This string is compatible with Source.Python's filters.
        """
        return ('un', 'spec', 't', 'ct')[self.team]

    @property
    def tf_team(self):
        """Get the player's Team Fortress team as a string.

        This string is compatible with Source.Python's filters.
        """
        return ('un', 'spec', 'red', 'blue')[self.team]

    def shift_property(self, prop_name, shift, duration=None):
        """Shift a player's integer property's value.

        Removes the inconvenience of using `setattr` and possibly other
        helper functions when trying to change a property's value
        via an other function (delays for example).
        If an optional duration argument is passed, the shift will be
        reverted after the duration has passed.
        """
        value = getattr(self, prop_name)
        setattr(self, prop_name, value + shift)
        if duration is not None:
            return Delay(duration, self.shift_property, prop_name, -shift)