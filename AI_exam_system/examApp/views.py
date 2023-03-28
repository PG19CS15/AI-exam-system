import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip


@gzip.gzip_page
def live_feed(request):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    cap.release()


def index(request):
    return StreamingHttpResponse(live_feed(request),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
