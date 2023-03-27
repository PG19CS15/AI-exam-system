import pyaudio
import webrtcvad
import collections
import numpy as np
import scipy.signal as signal
import noisereduce as nr

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
                frames_per_buffer=160,
                input_device_index=i) # replace DEVICE_INDEX with desired device index

# initialize VAD
vad = webrtcvad.Vad(3)
frames = collections.deque()

# Define bandpass filter parameters
low_freq = 80  # Lower cutoff frequency (in Hz)
high_freq = 300  # Upper cutoff frequency (in Hz)
filter_order = 4  # Filter order

# Create bandpass filter
b, a = signal.butter(filter_order, [low_freq / (8000/2), high_freq / (8000/2)], 'band')

# Define noise reduction parameters
hop_length = 256
n_fft = 512

while True:
    try:
        # read audio data from stream
        data = stream.read(160) # change this to match frames_per_buffer
        # convert to numpy array
        samples = np.frombuffer(data, dtype=np.int16)
        # apply bandpass filter
        filtered_samples = signal.filtfilt(b, a, samples)
        # perform noise reduction
        reduced_noise = nr.reduce_noise(y=filtered_samples, sr=8000, 
                                    hop_length=hop_length,
                                    n_fft=n_fft)


        # apply VAD on noise-reduced samples
        speech = vad.is_speech(reduced_noise.astype(np.int16).tobytes(), 8000)
        if speech:
            print("Voice detected!")
    except Exception as e:
        print(e)
        break

# stop stream and terminate pyaudio
stream.stop_stream()
stream.close()
p.terminate()
