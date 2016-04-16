
MAX_BREAK_BETWEEN_TWO_SIGNALS = 0.3
MAX_NUMBER_OF_POINTS_IN_GROUP = 3000
MAX_DURATION_OF_GROUP = 4

class SignalCollection:
    """Collection of signals (points) to interpret."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.signal_list = []

    def need_to_remove_first_signal_from_list(self, signal):
        if not self.signal_list:
            return False
        if len(self.signal_list) >= MAX_NUMBER_OF_POINTS_IN_GROUP:
            return True
        duration = signal.get_time() - self.signal_list[0].get_time()
        if duration > MAX_DURATION_OF_GROUP:
            return True
        return False

    def add_new_signal_and_remove_too_old_signals(self, touchpad_signal):
        while self.need_to_remove_first_signal_from_list(touchpad_signal):
            self.signal_list.pop(0)
        self.signal_list.append(touchpad_signal)

    def too_much_time_passed(self, new_signal_time):
        if self.signal_list:
            duration = new_signal_time - self.signal_list[-1].get_time()
            if duration > MAX_BREAK_BETWEEN_TWO_SIGNALS:
                return True
        return False

    def as_list(self):
        return self.signal_list

