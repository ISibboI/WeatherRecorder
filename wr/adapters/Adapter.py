from abc import abstractmethod


class Adapter:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def _receive_data_(self):
        """
        Receives current weather data.
        :returns A list of tuples (timestamp in seconds, temperature, humidity, air pressure)
        """
        pass

    def receive_data(self):
        data = self._receive_data_()

        for point in data:
            if point.temperature > 100 or point.temperature < -40:
                raise RuntimeError('Temperature out of range: ' + str(point.temperature))

            if point.humidity > 100 or point.humidity < 0:
                raise RuntimeError('Humidity out of range: ' + str(point.humidity))

            if point.pressure > 1100 or point.pressure < 900:
                raise RuntimeError('Pressure out of range: ' + str(point.pressure))

        return data
