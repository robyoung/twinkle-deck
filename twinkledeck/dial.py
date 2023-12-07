class Dial:
    def __init__(self, adc, min, max):
        """
        Args:
            pin (int): ADC pin number
            min (int): Maximum observed value of the knob
            max (int): Minimum observed value of the knob
        """
        self.adc = adc
        self._min = min
        self._max = max

    @property
    def value(self):
        return (self.adc.read_u16() - self._min) / (self._max - self._min)

