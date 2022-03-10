"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation='', name='', diameter=float('nan'), hazardous=''):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation for this NearEarthObject.  -> str
        :param name: The IAU name for this NearEarthObject.  -> str
        :param diameter: The diameter, in kilometers, of this NearEarthObject.  -> float
        :param hazardous: Whether or not this NearEarthObject is potentially hazardous.  -> bool
        """
        if not isinstance(designation, str):
            raise TypeError("'designation' must be a string.")

        if not isinstance(name, str):
            raise TypeError("'name' must be a string.")

        if not isinstance(diameter, (float, int)):
            raise TypeError("'diameter' must be a number.")

        if not isinstance(hazardous, (bool, str)):
            raise TypeError("'hazardous' must be True/False.")

        self.designation = designation if designation else None
        self.name = name if name else None
        self.diameter = diameter
        self.hazardous = hazardous == 'Y'

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f'{self.designation} ({self.name})'
        else:
            return f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return f'NEO {self.fullname} has a diameter of {self.diameter:.3f} km and is potentially hazardous.'
        else:
            return f'NEO {self.fullname} has a diameter of {self.diameter:.3f} km and is not potentially hazardous.'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject({self.designation=!r}, {self.name=!r}, " \
               f"{self.diameter=:.3f}, {self.hazardous=!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation='', time='', distance=float('nan'), velocity=float('nan'), neo=None):
        """Create a new `CloseApproach`.

        :param designation: The primary designation for this NearEarthObject.  -> str
        :param time: The date and time, in UTC, at which the NEO passes closest to Earth. -> str
        :param distance: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point. -> float
        :param velocity: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point. -> float
        :param neo: The NearEarthObject that is making a close approach to Earth. -> None
        """
        if not isinstance(designation, str):
            raise TypeError("'designation' must be a string.")

        if not isinstance(time, str):
            raise TypeError("'time' must be a string in the following format; 'yyyy-mm-dd HH:MM'.")

        if not isinstance(velocity, (float, int)):
            raise TypeError("'velocity' must be a number.")

        if not isinstance(distance, (float, int)):
            raise TypeError("'distance' must be a number.")

        self._designation = designation if designation else None
        self.time = cd_to_datetime(time) if time else None
        self.distance = float(distance)
        self.velocity = float(velocity)

        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        str_time = datetime_to_str(self.time) if self.time else ''
        return str_time

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance " \
               f"of {self.distance=:.2f} au and a velocity of {self.velocity=:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
