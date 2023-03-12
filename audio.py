import pyaudio
import webrtcvad
import collections
import numpy as np
# initialize pyaudio and open stream
p = pyaudio.PyAudio()

# List all available input devices
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:
        print(f"Device index: {i}, Device name: {device_info['name']}")
        break
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=8000,
                input=True,
                frames_per_buffer=80,
                input_device_index=i) # replace DEVICE_INDEX with desired device index

# initialize VAD
vad = webrtcvad.Vad(2)
frames = collections.deque()

while True:
    # read audio data from stream
    data = stream.read(80) # change this to match frames_per_buffer
    # convert to numpy array
    samples = np.frombuffer(data, dtype=np.int16)
    # apply VAD on samples
    speech = vad.is_speech(samples.tobytes(), 8000)
    if speech:
        print("Voice detected!")