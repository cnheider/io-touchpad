# -*- coding: utf-8 -*-

"""A collection of signals.

A signal is an item taken out of the queue. It might be something more than a
touchpad event.
"""
import os
import pickle

STANDARD_MAX_BREAK_VALUE = 0.3

MAX_NUMBER_OF_SIGNALS_IN_GROUP = 3000
MAX_DURATION_OF_GROUP = 4

DATA_PATH = 'signalcollection/data/'
EXPORT_PATH = 'signalcollection/exports/'

class SignalCollection:
    """Collection of signals to interpret.

    Attributes:
        signal_list (list): A list of signals chronologically. Old signals
            are regularly removed.
    """

    def __init__(self):
        """Constructor.

        Simply initializes an empty list.
        """
        self.max_waittime = STANDARD_MAX_BREAK_VALUE
        self.is_ending_on_raise = False
        self.reset()
        self.load_settings()

    def load_settings(self):
        """Load saved settings from file.

        loads MAX_NUMBER_OF_SIGNALS_IN_GROUP
        and END_ON_RAISE.
        """
        if os.path.exists(DATA_PATH):
            if os.path.isfile(DATA_PATH + 'MAX_BREAK_BETWEEN_TWO_SIGNALS'):
                handle = open(DATA_PATH + 'MAX_BREAK_BETWEEN_TWO_SIGNALS',
                              'rb')
                self.max_waittime = pickle.load(handle)
            else:
                self.max_waittime = STANDARD_MAX_BREAK_VALUE
            if os.path.isfile(DATA_PATH + 'END_ON_RAISE'):
                handle = open(DATA_PATH + 'END_ON_RAISE', 'rb')
                self.is_ending_on_raise = pickle.load(handle)
            else:
                self.is_ending_on_raise = False
        else:
            self.max_waittime = STANDARD_MAX_BREAK_VALUE
            self.is_ending_on_raise = False

    def save_settings(self):
        """Save saved settings from file.

        saves MAX_NUMBER_OF_SIGNALS_IN_GROUP
        and END_ON_RAISE.
        """
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
        with open(DATA_PATH + 'MAX_BREAK_BETWEEN_TWO_SIGNALS', 'wb') as handle:
            pickle.dump(self.max_waittime, handle)
        with open(DATA_PATH + 'END_ON_RAISE', 'wb') as handle:
            pickle.dump(self.is_ending_on_raise, handle)

    def set_max_break_between_two_signals(self, new_value):
        """Set new max_break_between_two signals and save settings."""

        if new_value > 0:
            self.max_waittime = new_value
            self.is_ending_on_raise = False

        elif new_value == 0:
            print("Setting end on raise finger")
            self.is_ending_on_raise = True

        self.save_settings()

    def import_settings(self, settings_name):
        """Load saved settings from file.

        imports MAX_NUMBER_OF_SIGNALS_IN_GROUP
        and END_ON_RAISE.
        """
        print("importing in signalcollection")

        if os.path.exists(EXPORT_PATH) and \
                os.path.isfile(EXPORT_PATH + settings_name):
            handle = open(EXPORT_PATH + settings_name, 'rb')
            imported = pickle.load(handle)
            self.max_waittime = imported[0]
            self.is_ending_on_raise = imported[1]
        self.save_settings()

    def export_settings(self, settings_name):
        """Save saved settings from file.

        exports MAX_NUMBER_OF_SIGNALS_IN_GROUP
        and END_ON_RAISE.
        """
        print("exporting in signalcollection")

        exported = [self.max_waittime, self.is_ending_on_raise]
        if not os.path.exists(EXPORT_PATH):
            os.makedirs(EXPORT_PATH)
        with open(EXPORT_PATH + settings_name, 'wb') as handle:
            pickle.dump(exported, handle)

    def is_ending_on_raise(self):
        """Return if the signal should end on raising finger."""

        return self.is_ending_on_raise

    def reset(self):
        """Erase the signal_list."""
        self.signal_list = []

    def add_and_maintain(self, signal):
        """Remove some signals and add a new one.

        Remove signals from the head of the signal_list if they are old
        or if there are too many of them.

        Args:
            signal (TouchpadSignal): A new signal to be added.
        """
        while self._need_to_remove_head(signal):
            self.signal_list.pop(0)
        self.signal_list.append(signal)

    def is_recent_enough(self, current_time):
        """Check if the last signal is recent enough.

        Compares the time of the occurance of the tail signal with the
        current time.

        Args:
            current_time (float): The current time which is compared with
                the time of the last signal in the list.

        Retruns:
            True if the (current_time - tail_time) is less or equal
            MAX_BREAK_BETWEEN_TWO_SIGNALS.
            True is returned if the signal_list
            is empty. False otherwise.
        """
        try:
            tail_time = self.signal_list[-1].get_time()
        except IndexError:
            result = True
        else:
            result = current_time - tail_time <= \
                     self.max_waittime
        return result

    def get_max_break_between_two_points(self):
        """Get max timewait."""

        return self.max_waittime

    def get_time_when_old_enough(self, current_time):
        """Get the amount of time left for the tail to get old.

        The tail is the tail of the signal_list.

        Args:
            current_time (float): The current time which is compared with
                the time of the last signal in the list.

        Returns:
            The difference between the current time and the time of the tail.
            None is returned if the signal_list is empty.
        """
        try:
            tail_time = self.signal_list[-1].get_time()
        except IndexError:
            result_time = None
        else:
            result_time = current_time - tail_time
        return result_time

    def as_list(self):
        """Return the SignalCollection as a list.

        Returns:
            The signal_list as a list.
        """
        return self.signal_list

    def _need_to_remove_head(self, signal):
        """Check if there is a need of the list's head removal.

        Args:
            signal (TouchpadSignal): A signal. Needed to calculate if the head
                is too old or not.

        Returns:
            True if the list is too big or if the head is too old.
            False otherwise.
        """
        if self._is_empty():
            return False
        elif self._is_too_big():
            return True
        elif self._is_head_too_old(signal):
            return True
        else:
            return False

    def _is_empty(self):
        """Check if the signal_list is empty.

        Returns:
            True if signal list is empty. False otherwise.
        """
        return self.signal_list == []

    def _is_too_big(self):
        """Check if the signal_list is not too big.

        Returns:
            True if signal list is too big. False otheriwse.
        """
        return len(self.signal_list) >= MAX_NUMBER_OF_SIGNALS_IN_GROUP

    def _is_head_too_old(self, signal):
        """Check if the head of the signal_list is too old.

        Args:
            signal (TouchpadSignal): A signal which is compared with the head
                in terms of the time attribute.

        Returns:
            True if the head of signal list is too old.
        """
        signal_time = signal.get_time()
        head_time = self.signal_list[0].get_time()
        return signal_time - head_time > MAX_DURATION_OF_GROUP
