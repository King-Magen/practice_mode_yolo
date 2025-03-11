import cv2 
from ultralytics import YOLO
import cvzone  
 

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y] 

model = YOLO("yolo11n.pt")
names=model.model.names

USERNAME = "admin"
PASSWORD = "Admin!123"
IP_ADD = "192.168.100.53" #this is for office / 192.168.100.69 for production
PORT = 544

# rtspLive = f'rtsp://{USERNAME}:{PASSWORD}@192.168.100.53:544/Streaming/Channels/1001/'
rtspLive = f'rtsp://admin:Admin!123@192.168.100.53:554/Streaming/Channels/1001/'
cap = cv2.VideoCapture(rtspLive, cv2.CAP_FFMPEG) 

entering_ids = set()
exiting_ids = set()
person_status = {}  
c_entry = 300  
c_exit = 700  
person_count = set()
current_detected = 0

while True:
    ret,frame = cap.read()
    if not ret:
        print("Frame not received, check stream.")
        break 
    
    frame = cv2.resize(frame, (1020, 600))
    # Run YOLO11 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True, conf=0.2, iou=0.7, classes=0, imgsz=1280)

    # Check if there are any boxes in the results
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
        track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score

        current_detected = len(track_ids)

        for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
            c = names[class_id]
            x1, y1, x2, y2 = box 
            # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            cx = (x1 + x2) // 2
            text_size = cv2.getTextSize(f'{track_id}', cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            text_x = cx + (text_size[1] // 2)

            cvzone.putTextRect(frame, f'{track_id}', (cx, y2), 1, 1, colorT=(255, 255, 255), colorR=(0, 96, 143))
            person_count.add(track_id)

            # cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center point 
            # if track_id not in person_status:
            #     person_status[track_id] = cx  # Store initial Y position

            # previous_cx = person_status[track_id]
            # person_status[track_id] = cx  # Update position

            # if previous_cx < c_entry and cx >= c_entry:  # If person crosses entry line from top
            #     entering_ids.add(track_id)
            # if previous_cx > c_exit and cx <= c_exit:  # If person crosses exit line from bottom
            #     exiting_ids.add(track_id) 

        # Draw entry and exit lines
        # cv2.line(frame, (c_entry, 0), (c_entry, 600), (0, 255, 0), 2)  # Green entry line
        # cv2.line(frame, (c_exit, 0), (c_exit, 600), (0, 0, 255), 2)  # Red exit line
        cvzone.putTextRect(frame, f'Detected Persons: {current_detected}', (50, 50), 1, 1, colorT=(255, 255, 255), colorR=(0, 96, 143))
        # cvzone.putTextRect(frame, f'Total Persons: {len(person_count)}', (50, 100), 1, 1, colorT=(255, 255, 255), colorR=(0, 96, 143))

    cv2.imshow("Practice mode", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
       break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
