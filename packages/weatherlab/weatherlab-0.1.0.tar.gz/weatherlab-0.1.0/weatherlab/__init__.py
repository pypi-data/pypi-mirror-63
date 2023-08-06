from .extension import WeatherLabExtension
from .magics import MagicWeatherLab
from .version import VERSION

__version__ = ".".join(VERSION)


def load_ipython_extension(ipython):
    ipython.register_magics(MagicWeatherLab)

    weatherlab = WeatherLabExtension(ipython)
    weatherlab.register_comm()


def unload_ipython_extension(ipython):  # pylint: disable=W0613
    pass
