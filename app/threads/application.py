import queue
import time
def application_thread(collection, queue):
    """The application thread.

    It receives signals/events from the listener thread using a queue and then
    interprets the data.
    """
    # main loop - in every iteration one signal is read,
    # or too long break in signal streaming is captured
    while 1:
        while queue.empty() and not collection.too_much_time_passed(time.time()):
            pass

        is_new_signal = not queue.empty()

        if is_new_signal:
            signal = queue.get()

        if not(is_new_signal) or signal.is_it_stop_signal():
            send_points_to_interpreter(collection.as_list())
            collection.reset()
        elif collection.too_much_time_passed(signal.get_time()):
            send_points_to_interpreter(collection.as_list())
            collection.reset()
            if signal.is_it_proper_signal_of_point():
                collection.add_new_signal(signal)
        else:
            if signal.is_it_proper_signal_of_point():
                collection.add_new_signal_and_remove_too_old_signals(signal)



def send_points_to_interpreter(signal_list):
    """Interpret the signals from the signal list.

    At the moment the function is not interpreting anything. It just prints the
    first 10 points/events/signals from the signal_list.

    :param signal_list: List of read events.
    """
    if not signal_list:
        return
    print("New portion of events:")
    counter = 0
    length = len(signal_list)
    for one_signal in signal_list:
        counter += 1
        if counter == 11:
            print("...")
            break
        print("Event #", counter, "\tout of", length, "in the list. x:",
              one_signal.get_x(), "y:", one_signal.get_y())
    print()
