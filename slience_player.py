from multiprocessing import Process, Event
import numpy as np

class SilencePlayer(Process):
	def __init__(self, device, quitEvent : Event):
		super(SilencePlayer, self).__init__()
		self.quitEvent = quitEvent
		self.device = device

	def run(self):
		while True:
			self.device.play(np.zeros((512, 2)), samplerate=48000, channels=[0, 1])

			if self.quitEvent.is_set():
				return