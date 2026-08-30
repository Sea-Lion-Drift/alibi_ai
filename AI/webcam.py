import cv2
from ultralytics import YOLO
from AI.stats import interview_stats

# ==========================
# Load YOLO Model
# ==========================

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_counter = 0

last_person_count = 0
last_phone_detected = False


def generate_frames():

    global frame_counter
    global last_person_count
    global last_phone_detected

    while True:

        success, frame = camera.read()

        if not success:
            break

        interview_stats["total_frames"] += 1

        frame_counter += 1

        frame = cv2.resize(frame, (640, 480))

        # Use previous values for skipped frames
        person_count = last_person_count
        phone_detected = last_phone_detected

        # Run YOLO every 2nd frame
        if frame_counter % 2 == 0:

            person_count = 0
            phone_detected = False



            results = model(
                frame,
                imgsz=640,
                conf=0.25,
                verbose=False
            )

            for result in results:

                for box in result.boxes:

                    cls = int(box.cls[0])

                    class_name = model.names[cls]

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # ==========================
                    # PERSON
                    # ==========================

                    if class_name == "person":

                        person_count += 1

                        interview_stats["eye_contact_frames"] += 1

                        #cv2.rectangle(
                           # frame,
                            #(x1, y1),
                            #(x2, y2),
                            #(0,255,0),
                           # 2
                        #)

                        #cv2.putText(
                            #frame,
                           # "PERSON",
                          #  (x1,y1-10),
                            #cv2.FONT_HERSHEY_SIMPLEX,
                            #0.7,
                            #0,255,0),
                            #2
                        #)

                    # ==========================
                    # PHONE
                    # ==========================

                    elif class_name == "cell phone":

                        phone_detected = True

                        interview_stats["phone_detected"] = True

                        #cv2.rectangle(
                         #   frame,
                          #  (x1,y1),
                           # (x2,y2),
                            #(0,0,255),
                            #3
                        #)

                        #cv2.putText(
                         #   frame,
                          #  "PHONE",
                           # (x1,y1-10),
                            #cv2.FONT_HERSHEY_SIMPLEX,
                            #0.7,
                            #(0,0,255),
                            #2
                        #)

            # Save latest detections
            last_person_count = person_count
            last_phone_detected = phone_detected

        interview_stats["multiple_faces"] = person_count > 1

        # ==========================
        # STATUS
        # ==========================



        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )