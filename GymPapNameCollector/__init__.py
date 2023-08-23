__author__ = "AlbertUnruh"
__version__ = "0.0.0a"
__license__ = "GNU AGPLv3"
__copyright__ = f"Copyright 2023-present (c) {__author__}"
__url__ = "https://github.com/AlbertUnruh/GymPap-NameCollector"


from vendor.AlbertUnruhUtils.utils.logger import get_logger

__root_logger__ = get_logger(None, level=0)


from .constants import *
from .worldwidewifi import *


# crime section

__USER_AGENT = USER_AGENT
USER_AGENT = USER_AGENT.format(**globals())
# should be a *constant* by definition, but crimes have to be committed ^^
__root_logger__.info(f"Set `USER_AGENT` from {__USER_AGENT!r} to {USER_AGENT!r}")
__root_logger__.debug(f"A copy of the original `USER_AGENT` has been set in `__USER_AGENT`")
