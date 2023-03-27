import cv2
import pyaudio
import wave
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = 640
frame_height = 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
out = cv2.VideoWriter('output.avi', fourcc, 24.0, (frame_width, frame_height))
audio = pyaudio.PyAudio()
audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk = 1024

stream = audio.open(format=audio_format, channels=channels,
                    rate=sample_rate, input=True, frames_per_buffer=chunk)

is_recording = False

wf = wave.open('output.wav', 'wb')
wf.setnchannels(channels)
wf.setsampwidth(audio.get_sample_size(audio_format))
wf.setframerate(sample_rate)

while True:

    ret, frame = cap.read()

    cv2.imshow('Video Feed', frame)

    audio_data = stream.read(chunk)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        is_recording = True
        print('Recording started...')

    if is_recording:
        out.write(frame)
        wf.writeframes(audio_data)
    
    elif key == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()


stream.stop_stream()
stream.close()
audio.terminate()
wf.close()


video_clip = VideoFileClip('output.avi')
audio_clip = AudioFileClip('output.wav')
audio_clip = audio_clip.set_fps(30)
final_clip = video_clip.set_audio(audio_clip)
final_clip.write_videofile('output1.mp4')

video_clip.close()
audio_clip.close()

