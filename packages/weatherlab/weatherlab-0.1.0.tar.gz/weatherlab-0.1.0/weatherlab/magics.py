from IPython.core.magic import Magics, line_magic, magics_class, needs_local_scope


@magics_class
class MagicWeatherLab(Magics):
    @line_magic
    @needs_local_scope
    def weather_lab_data(self, line, local_ns):  # pylint: disable=W0613,R0201
        if "WEATHER_LAB_DATA" in local_ns:
            if local_ns["WEATHER_LAB_DATA"] is None:
                print(
                    "It appears that you don't have weatherlab jupyterlab "
                    "extension or maybe you doesn't run a search yet"
                )
            return local_ns["WEATHER_LAB_DATA"]
        return None
