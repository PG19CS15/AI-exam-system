import cv2
import pyaudio
import wave
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Set the video codec and frame size
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = 640
frame_height = 480

# Define the video capture object
cap = cv2.VideoCapture(0)

# Set the frame rate of the video capture object
cap.set(cv2.CAP_PROP_FPS, 30)

# Define the video writer object
out = cv2.VideoWriter('output.avi', fourcc, 24.0, (frame_width, frame_height))

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Set audio parameters
audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk = 1024

# Open the audio stream
stream = audio.open(format=audio_format, channels=channels,
                    rate=sample_rate, input=True, frames_per_buffer=chunk)

# Initialize the recording flag
is_recording = False

# Initialize the WAV file writer
wf = wave.open('output.wav', 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio.get_sample_size(audio_format))
wf.setframerate(sample_rate)

while True:
    # Capture each frame of the video feed
    ret, frame = cap.read()
    
    # Display the frame in a window
    cv2.imshow('Video Feed', frame)
    
    # Read audio data from the stream
    audio_data = stream.read(chunk)
    
    # Check for key press events
    key = cv2.waitKey(1) & 0xFF
    
    # If the 'r' key is pressed, start recording
    if key == ord('r'):
        is_recording = True
        print('Recording started...')
    
    # If the 's' key is pressed, stop recording
    elif key == ord('s'):
        is_recording = False
        print('Recording stopped.')
    
    # If recording is enabled, write the frame and audio data to the video writer and WAV file respectively
    if is_recording:
        out.write(frame)
        wf.writeframes(audio_data)
    
    # If the 'q' key is pressed, quit the program
    elif key == ord('q'):
        break

# Release the resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Close the audio stream and WAV file
stream.stop_stream()
stream.close()
audio.terminate()
wf.close()

# Merge the video and audio files using moviepy
video_clip = VideoFileClip('output.avi')
audio_clip = AudioFileClip('output.wav')
audio_clip = audio_clip.set_fps(30)
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile('output1.mp4')

# Delete the intermediate files
video_clip.close()
audio_clip.close()
os.remove('output.avi')
os.remove('output.wav')