class TouchpadSignal:
    """Wrapper for the struct touchpad_event from touchpadlib.

    :param x
    :param y
    :param pressure
    :param time
    """

    def __init__(self, x, y, pressure, time):
        self.x = x
        self.y = y
        self.pressure = pressure
        self.time = time

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_time(self):
        return self.time

    def is_it_stop_signal(self):
        # TODO Implement this method. Not in the first iteration.
        # We could set condition pressure<1 but for now the only reason
        # to end the group is a long break between signals.
        return False

    def is_it_proper_signal_of_point(self):
        return self.x >= 0 and self.y >= 0

