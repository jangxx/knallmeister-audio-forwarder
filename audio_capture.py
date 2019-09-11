import soundcard as sc

def getDevices():
	devices = []

	for device in sc.all_microphones(include_loopback=True):
		if not device.isloopback:
			continue

		devices.append({
			"name": device.name,
			"device": device
		})

	return devices

def startCapture(deviceIndex, log_function):
	pass