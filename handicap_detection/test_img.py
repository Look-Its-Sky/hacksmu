from ultralytics import YOLO
import cv2, time

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

def process_image(image_path):
    global font, counter, fps, annotated_frame, height, weight, pos 
    confidence = 0.45
    
    tStart = time.time()
    frame = cv2.imread(image_path)
    annotated_frame = frame

    if frame is not None:
        hc_results = hc_model(frame)

        for result in hc_results:
            annotated_frame = result.plot()

        if len(hc_results) > 0:
            car_results = car_model(annotated_frame, conf=confidence)
            for result in car_results:
                annotated_frame = result.plot()

        tEnd = time.time()
        loopTime = tEnd - tStart
        fps = .9 * fps + .1 * (1/loopTime)
        # cv2.putText(annotated_frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)

        cv2.imshow('Frame', annotated_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Unable to read the image.")

process_image('IMG_3841.jpg')
