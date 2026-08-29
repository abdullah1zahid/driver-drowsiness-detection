import cv2
import mediapipe as mp
import winsound
from scipy.spatial import distance as dist

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]


def calculate_ear(eye_points, landmarks, frame_width, frame_height):
    coords = []
    for idx in eye_points:
        lm = landmarks[idx]
        x = int(lm.x * frame_width)
        y = int(lm.y * frame_height)
        coords.append((x, y))

    vertical_1 = dist.euclidean(coords[1], coords[5])
    vertical_2 = dist.euclidean(coords[2], coords[4])
    horizontal = dist.euclidean(coords[0], coords[3])

    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear


# تھریش ہولڈ اور کاؤنٹر سیٹنگز
EAR_THRESHOLD = 0.20
EAR_CONSEC_FRAMES = 20
closed_frames = 0

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        print("Camera not found!")
        break

    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            left_ear = calculate_ear(LEFT_EYE, landmarks, frame_width, frame_height)
            right_ear = calculate_ear(RIGHT_EYE, landmarks, frame_width, frame_height)

            avg_ear = (left_ear + right_ear) / 2.0

            # لاجک: دونوں آنکھیں بند ہونے پر کاؤنٹر اور الرٹ
            if left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
                closed_frames += 1
                if closed_frames >= EAR_CONSEC_FRAMES:
                    # سکرین پر الرٹ اور سپیکر سے بیپ
                    cv2.putText(frame, "DROWSINESS ALERT!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    winsound.Beep(1000, 200)
            else:
                closed_frames = 0

            # سکرین پر میٹرکس ڈسپلے کرنا
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Closed Frames: {closed_frames}/{EAR_CONSEC_FRAMES}", (30, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Driver Drowsiness Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()