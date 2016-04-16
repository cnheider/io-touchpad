import _thread

from touchpadsignal import touchpadsignal

def start(queue):
    _thread.start_new_thread(listener_thread, (queue,))


def listener_thread(queue):
    """The main function of the listener thread.

    The listener thread fetches events from the touchpad and pushes them onto
    the queue.
    """

    while 1:
        touchpad_signal = touchpadsignal.TouchpadSignal()
        queue.put(touchpad_signal, True)
