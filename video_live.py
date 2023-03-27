import cv2

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Set the video codec and frame size
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the video writer object
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

# Initialize the recording flag
is_recording = False

while True:
    # Capture each frame of the video feed
    ret, frame = cap.read()
    
    # Display the frame in a window
    cv2.imshow('Video Feed', frame)
    
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
    
    # If recording is enabled, write the frame to the video writer object
    if is_recording:
        out.write(frame)
    
    # If the 'q' key is pressed, quit the program
    elif key == ord('q'):
        break

# Release the resources
cap.release()
out.release()
cv2.destroyAllWindows()