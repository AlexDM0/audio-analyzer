#!/usr/bin/env python3
import numpy as np
import sounddevice as sd
import soundfile as sf
import queue
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants.Constants import THRESHOLD, SNAPSHOT_DURATION
from util.FileUtil import save_volume_data, store_audio
from util.QueueUtil import audioQueue, clear_queue
from pathlib import Path
import os

baseDir = os.path.dirname(__file__)

os.makedirs(os.path.join(baseDir,'data'), exist_ok=True)
os.makedirs(os.path.join(baseDir,'snapshots'), exist_ok=True)

# Initialize the list to store timestamp and volume_norm
volume_data = []
max_volume = 0
store_snapShot = False


sample_rate = sd.query_devices(sd.default.device, 'input')['default_samplerate']
print(f"Default samplerate: {sample_rate} Hz\n")


def audio_callback(indata, frames, frameTime, status):
    global store_snapShot
    global volume_data
    global max_volume
    audioQueue.put(indata.copy())
    volume_norm = np.linalg.norm(indata) * 10
    timestamp = time.time()
    max_volume = max(max_volume, volume_norm)

    volume_data.append((timestamp, int(volume_norm)))

    # yf = fft(indata)
    if volume_norm > THRESHOLD:
        store_snapShot = True


stream = sd.InputStream(callback=audio_callback,samplerate=sample_rate, channels=1)

# Set up the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'b-')
threshold_line = ax.axhline(y=THRESHOLD, color='r', linestyle='--')
# Record the start time
start_time = time.time()

def update(frame):
    global max_volume, ax, ln
    if volume_data:
        xdata.append(volume_data[-1][0] - start_time)
        ydata.append(volume_data[-1][1])
        ln.set_data(xdata, ydata)
        if xdata[0] != xdata[-1]:
            ax.set_xlim(xdata[0], xdata[-1])
        if 0 != max_volume:
            ax.set_ylim(0, max_volume)
    return ln,

ani = FuncAnimation(fig, update, blit=False, interval=100, cache_frame_data=False)
plt.ion()

snapshot_start_time = time.time()
RUNNING = True

def on_close(event):
    global RUNNING
    RUNNING = False

fig.canvas.mpl_connect('close_event', on_close)

with stream:
    print("Recording started")
    while RUNNING:
        try:
            sd.sleep(100)
            plt.show()
            plt.pause(0.001)
            print("Recording..." + str(time.time() - snapshot_start_time))
            if (time.time() - snapshot_start_time) > SNAPSHOT_DURATION:
                if store_snapShot:
                    print("Storing snapshot")
                    store_audio(audioQueue, sample_rate)
                    store_snapShot = False
                else:
                    print("clearing snapshot")
                    clear_queue(audioQueue)
                snapshot_start_time = time.time()
            save_volume_data(volume_data)
            volume_data.clear()

        except KeyboardInterrupt:
            print("Interrupted by user")
            break

if store_snapShot:
    print("Storing snapshot")
    store_audio(audioQueue, sample_rate)
