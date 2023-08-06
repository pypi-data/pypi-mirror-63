class WeatherLabExtension:
    def __init__(self, ipython):
        self.ipython = ipython
        self.ipython.push({"WEATHER_LAB_DATA": None})

    def callback(self, comm, msg):
        @comm.on_msg
        def _recv(msg):
            self.ipython.push(msg["content"]["data"])

        comm.send({"msgtype": "WeatherLab-Kernel", "message": msg})

    def register_comm(self):
        self.ipython.kernel.comm_manager.register_target("weatherlab", self.callback)
