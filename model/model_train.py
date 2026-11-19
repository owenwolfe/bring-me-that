from ultralytics import YOLO

#Load a model here
model = YOLO("yolo26s.pt")

#Train model with custom dataset
# results = model.train(data="/research/jortizguzman/CSCI585/model/data.yaml", epochs=100, imgsz=640) #train1.pt
results = model.train(data="/research/jortizguzman/CSCI585/model/data.yaml", epochs=100, imgsz=640, optimizer="Adam", lr0=0.0001) #train2
