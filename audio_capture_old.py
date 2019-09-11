import pyaudio
import asyncio
import sys

audio = pyaudio.PyAudio()

def getDevices():
    devices = []

    try:
        default_index = audio.get_default_input_device_info()["index"]
    except IOError:
        default_index = -1

    selection_index = -1
    j = 0

    for i in range(audio.get_device_count()):
        devInfo = audio.get_device_info_by_index(i)

        if sys.platform == "win32":
            if devInfo["maxOutputChannels"] == 0 or audio.get_host_api_info_by_index(devInfo["hostApi"])["name"].find("WASAPI") == -1:
                continue
        else:
            if devInfo["maxInputChannels"] == 0:
                continue

        if default_index < 0:
            default_index = i

        if default_index == i:
            selection_index = j

        devices.append({
            "name": devInfo["name"],
            "index": devInfo["index"],
        })

        j += 1

    return (devices, selection_index)

def startCapture(deviceIndex, log_function):
    info = audio.get_device_info_by_index(deviceIndex)

    if sys.platform == "win32":
        stream = audio.open(format = pyaudio.paFloat32,
                            channels = 1,
                            rate = int(info["defaultSampleRate"]),
                            input = True,
                            frames_per_buffer = 512,
                            input_device_index = info["index"],
                            as_loopback = True)
    else:
        stream = audio.open(format = pyaudio.paFloat32,
                            channels = 1,
                            rate = int(info["defaultSampleRate"]),
                            input = True,
                            frames_per_buffer = 512,
                            input_device_index = info["index"])

    return stream

def close():
    audio.terminate()