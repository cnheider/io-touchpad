#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import _thread
import queue
import time
MAX_NUMBER_OF_POINTS_IN_GROUP = 3
MAX_DURATION_OF_GROUP = 4
MAX_BREAK_BETWEEN_TWO_SIGNALS = 0.3

# TODO modification of signal structure
# signal structure
class TouchpadSignal:
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
		return False  # we could set condition pressure<1 but for now the only reason to end the group is a long break between signals


# signal queue
queue = queue.Queue()

# thread which catches signals from touchpad and put it on queue 
def listener_thread() :
	# TODO touchpadlib init
	while 0: # change to "while 1" when it will be ready
		# TODO touchpad_signal = get signal from touchpadlib
		queue.put(touchpad_signal, True)
	# temporary
	counter = 0
	while counter < 11:
		counter += 1
		counter %= 100
		time.sleep(.2)
		if counter % 5 == 0:
			queue.put(TouchpadSignal(0, 0, 0.5, time.time()), True)
		else:
			queue.put(TouchpadSignal(2, 3, 3, time.time()), True)

# here will be parsing and sending list of signals to interpreter, for now printing points
def send_points_to_interpreter(signal_list):
	if not signal_list:
		return
	print ("new portion of points:")
	for one_signal in signal_list:
		print ("x: %d y: %d" % ( one_signal.get_x(), one_signal.get_y() ) )

# list of signals (points) to interpret
signal_list = []

def init_signal_list():
	global signal_list
	signal_list = []

def need_to_remove_first_signal_from_list(touchpad_signal_to_add):
	global signal_list
	if not signal_list:
		return False
	return len(signal_list) >= MAX_NUMBER_OF_POINTS_IN_GROUP or touchpad_signal_to_add.get_time() - signal_list[0].get_time() > MAX_DURATION_OF_GROUP

def add_signal_to_list_and_remove_too_old_signals(touchpad_signal):
	global signal_list
	while need_to_remove_first_signal_from_list(touchpad_signal):
		signal_list.pop(0)   
	signal_list.append(touchpad_signal)

def too_much_time_passed(new_signal_time):
	if signal_list and new_signal_time - signal_list[-1].get_time() > MAX_BREAK_BETWEEN_TWO_SIGNALS:
		return True
	return False

# thread, which selects portion of signals from queue, and sends it to the interpreter
def application_thread():

	# main loop - in every iteration one signal is read, or too long break in signal streaming is captured
	while 1:
		while queue.empty() and not (too_much_time_passed(time.time())):
			pass

		is_new_signal = not (queue.empty())

		if is_new_signal: 
			touchpad_signal = queue.get()

		if not(is_new_signal) or touchpad_signal.is_it_stop_signal():
			send_points_to_interpreter(signal_list)
			init_signal_list()
		elif too_much_time_passed(touchpad_signal.get_time()):
			send_points_to_interpreter(signal_list)
			init_signal_list()
			add_signal_to_list_and_remove_too_old_signals(touchpad_signal)
		else:
			add_signal_to_list_and_remove_too_old_signals(touchpad_signal)
			


# running both threads

_thread.start_new_thread(listener_thread, () )
application_thread()




