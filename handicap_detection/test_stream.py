from ultralytics import YOLO
import cv2, time, random

counter = -1

fps = 30
font = cv2.FONT_HERSHEY_SIMPLEX
pos = (30, 60)
height = 1.5
weight = 3
myColor = (0, 0, 255)

# hc_model = YOLO('models/hc_best.pt') 
hc_model = YOLO('models/combined.pt')
car_model = YOLO('models/carproject.pt')
# handicap_sign_class = 'parking'
handicap_sign_class = 'Engelli'
filter_results = False
annotated_frame = None

def generate_frames():
    global font, counter, fps, annotated_frame, height, weight, pos 
    confidence = 0.45
    
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
            if counter % 1 == 0 or True:
                hc_results = hc_model(frame)

                for result in hc_results:
                    annotated_frame = result.plot()

                if len(hc_results) > 0:
                    car_results = car_model(annotated_frame, conf=confidence)
                    for result in car_results:
                        annotated_frame = result.plot()

                counter = -1
    
        tEnd = time.time()
        loopTime = tEnd - tStart
        fps = .9 * fps + .1 * (1/loopTime)
        cv2.putText(annotated_frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)

        cv2.imshow('Frame', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

generate_frames()
