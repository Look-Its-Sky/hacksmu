from flask import Flask, Response
from ultralytics import YOLO
import cv2, time, random

counter = -1

fps = 30
font=cv2.FONT_HERSHEY_SIMPLEX
pos=(30,60)
height=1.5
weight=3
myColor=(0,0,255)

app = Flask(__name__)
# hc_model = YOLO('models/hc_best.pt') 
hc_model = YOLO('models/combined.pt')
car_model = YOLO('models/carproject.pt')
# handicap_sign_class = 'parking'
handicap_sign_class = 'Engelli'
filter_results = False
annotated_frame = None
camera_id = random.randint(1, 1000)

def generate_frames():
    global font, counter, fps, annotated_frame, height, weight, pos 
    
    tStart = time.time()
    cap = cv2.VideoCapture('/dev/video0')  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 

    while True:
        success, frame = cap.read()
        annotated_frame = frame
        tStart = time.time()
        counter += 1

        if not success:
            break

        else: 
            if counter % 2 == 0:
                hc_results = hc_model(frame)

                for result in hc_results:
                    annotated_frame = result.plot()

                if len(hc_results) > 0:
                    car_results = car_model(annotated_frame, conf=0.5)
                    for result in car_results:
                        annotated_frame = result.plot()

                counter = -1
    
        tEnd = time.time()
        loopTime = tEnd - tStart
        fps = .9 * fps + .1 * (1/loopTime)
        cv2.putText(annotated_frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera_id')
def get_camera_id():
    global camera_id
    return camera_id

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
