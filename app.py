#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import _thread
import queue
import time
from ctypes import cdll
MAX_NUMBER_OF_POINTS_IN_GROUP = 3000
MAX_DURATION_OF_GROUP = 4
MAX_BREAK_BETWEEN_TWO_SIGNALS = 0.3

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

lib = cdll.LoadLibrary('./touchpadlib.so') # TODO error handle
touchpad_signal_object = lib.new_event()
fd = lib.initalize_touchpadlib_usage() # TODO error handle

# thread which catches signals from touchpad and put it on queue 
def listener_thread() :
	while 1: 
		lib.fetch_touchpad_event(fd, touchpad_signal_object) # TODO error handle
		x = lib.get_x(touchpad_signal_object)
		y = lib.get_y(touchpad_signal_object)
		pressure = lib.get_pressure(touchpad_signal_object)
		time = lib.get_seconds(touchpad_signal_object) + 0.000001 * lib.get_useconds(touchpad_signal_object) 
		#print("%d %d %d %.8f" % (x, y, pressure, time) )
		touchpad_signal = TouchpadSignal(x, y, pressure, time)
		queue.put(touchpad_signal, True)

# here will be parsing and sending list of signals to interpreter, for now printing first 10 points
def send_points_to_interpreter(signal_list):
	if not signal_list:
		return
	print ("new portion of points:")
	counter = 0
	le = len(signal_list)
	for one_signal in signal_list:
		counter += 1
		if counter == 11:
			print("...")
			break
		print ("%d / %d x: %d y: %d" % (counter, le, one_signal.get_x(), one_signal.get_y() ) )
	print()

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

def proper_signal_of_point(touchpad_signal):
	return touchpad_signal.get_x() >= 0 and touchpad_signal.get_y() >= 0

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
			if proper_signal_of_point(touchpad_signal):
				add_signal_to_list_and_remove_too_old_signals(touchpad_signal)
		else:
			if proper_signal_of_point(touchpad_signal):
				add_signal_to_list_and_remove_too_old_signals(touchpad_signal)
			


# running both threads

_thread.start_new_thread(listener_thread, () )
application_thread()

# TODO erase touchpad_signal_object on stop stript




