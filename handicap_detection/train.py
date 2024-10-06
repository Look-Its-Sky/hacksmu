from ultralytics import YOLO
import sys
import pickle 

model = YOLO('models/yolov8n.pt')
results = model.train(data='/home/jude/Nextcloud/Repos/hacksmu/cam/data/data.yaml', epochs=300)
model.save('models/yolov8n_tuned.pt')
