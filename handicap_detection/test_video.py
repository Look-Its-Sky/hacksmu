# from ultralytics import YOLO
# import cv2, time
#
# counter = -1
#
# fps = 30
# font = cv2.FONT_HERSHEY_SIMPLEX
# pos = (30, 60)
# height = 1.5
# weight = 3
# myColor = (0, 0, 255)
#
# # hc_model = YOLO('models/hc_best.pt') 
# hc_model = YOLO('models/combined.pt')
# car_model = YOLO('models/carproject.pt')
# # handicap_sign_class = 'parking'
# handicap_sign_class = 'Engelli'
# filter_results = False
# annotated_frame = None
#
# def process_video(video_path):
#     global font, counter, fps, annotated_frame, height, weight, pos 
#     confidence = 0.45
#
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Unable to open video file.")
#         return
#
#     while cap.isOpened():
#         tStart = time.time()
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Print frame dimensions for verification
#         print(f"Processing frame of size: {frame.shape[1]}x{frame.shape[0]}")
#
#         annotated_frame = frame
#
#         if frame is not None:
#             hc_results = hc_model(frame)
#
#             for result in hc_results:
#                 annotated_frame = result.plot()
#
#             car_results = car_model(annotated_frame, conf=confidence)
#             for result in car_results:
#                 annotated_frame = result.plot()
#
#             tEnd = time.time()
#             loopTime = tEnd - tStart
#             fps = .9 * fps + .1 * (1/loopTime)
#             cv2.putText(annotated_frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)
#
#             cv2.imshow('Frame', annotated_frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             print("Error: Unable to read the frame.")
#
#     cap.release()
#     cv2.destroyAllWindows()
#

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

def process_video(video_path):
    global font, counter, fps, annotated_frame, height, weight, pos 
    confidence = 0.45
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    while cap.isOpened():
        tStart = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        # Print frame dimensions for verification
        print(f"Processing frame of size: {frame.shape[1]}x{frame.shape[0]}")

        annotated_frame = frame

        if frame is not None:
            frame_height, frame_width = frame.shape[:2]
            hc_results = hc_model(frame, imgsz=(frame_width, frame_height))

            for result in hc_results:
                annotated_frame = result.plot()

            car_results = car_model(annotated_frame, conf=confidence, imgsz=(frame_width, frame_height))
            for result in car_results:
                annotated_frame = result.plot()

            tEnd = time.time()
            loopTime = tEnd - tStart
            fps = .9 * fps + .1 * (1/loopTime)
            cv2.putText(annotated_frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)

            cv2.imshow('Frame', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Unable to read the frame.")

    cap.release()
    cv2.destroyAllWindows()

# process_video('video.mp4')
process_video('/home/jude/Downloads/demo_video.mov')

# process_video('video.mp4')
process_video('/home/jude/Downloads/demo_video.mov')
