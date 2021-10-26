from ._POW import *
from ._POW import __doc__

# Set callback to let POW construct rpki.sundial.datetime objects.

from rpki.sundial import datetime as sundial_datetime
customDatetime(sundial_datetime)
del sundial_datetime
