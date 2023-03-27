import pyaudio
import wave
import threading
import keyboard

# Set audio parameters
audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Initialize the recording flag
is_recording = False

# Define the WAV file writer
wf = wave.open('output.wav', 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio.get_sample_size(audio_format))
wf.setframerate(sample_rate)

# Define the callback function for the audio stream


def callback(in_data, frame_count, time_info, status):
    global is_recording
    if is_recording:
        wf.writeframes(in_data)
    return (in_data, pyaudio.paContinue)


# Define the audio stream object
stream = audio.open(format=audio_format, channels=channels,
                    rate=sample_rate, input=True, frames_per_buffer=chunk,
                    stream_callback=callback)

# Start the audio stream
stream.start_stream()

# Define the function to start recording


def start_recording():
    global is_recording
    is_recording = True
    print('Recording started...')

# Define the function to stop recording


def stop_recording():
    global is_recording
    is_recording = False
    print('Recording stopped.')
    wf.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()


# Define a keyboard event listener to start and stop recording
keyboard.add_hotkey('r', start_recording)
keyboard.add_hotkey('s', stop_recording)

# Wait for user input to exit
input('Press enter to exit...  press r to start and s to stoprs')