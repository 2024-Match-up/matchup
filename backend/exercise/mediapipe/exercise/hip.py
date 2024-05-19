import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def dou_calculate_angle(a, b):
    a = np.array(a)  # 첫 번째 점
    b = np.array(b)  # 두 번째 점

    # 수평 벡터 계산
    horizontal_vector = np.array([1, 0])

    # 두 점 사이의 벡터 계산
    ab_vector = abs(b - a)

    # 두 벡터 사이의 각도 계산
    radians = np.arccos(
        np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector)))
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

# Curl counter variables
counter = 0 
sets = 0
feedback = None
position = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for left hip
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate angle for left hip
            left_angle = calculate_angle(left_hip, left_knee, left_ankle)

            # Visualize angle
            cv2.putText(image, str(left_angle), 
                        tuple(np.multiply(left_knee, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Get coordinates for right hip
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate angle for right hip
            right_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # 수평
            hor_hip_angle = dou_calculate_angle(left_hip, right_hip)

            # Visualize angle
            cv2.putText(image, str(right_angle), 
                        tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Curl counter logic
            if (left_angle > 160) and (right_angle > 160):
                position = "down"
            if (left_angle < 100) and (right_angle < 100) and (position == 'down'):
                position = "up"
                counter += 1
                print("Counter:", counter)
                if counter == 10:
                    sets += 1
                    counter = 0
            # 점수
            if hor_hip_angle <10:
                feeedback = "Good"
           
            elif hor_hip_angle >= 10:
                feedback = "Bad"

            list_ALL = [left_shoulder, 
                        right_shoulder,
                        left_hip, 
                        right_hip, 
                        left_knee, 
                        right_knee, 
                        left_ankle,
                        right_ankle,
                        feedback]

            # 실시간 좌표값 측정
            print(list_ALL)

        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (700,73), (245,117,16), -1)

        # Rep data
        cv2.putText(image, 'REPS: ' , (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(counter), (15,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(image, 'POSITION: ' , (190, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, position, (185,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        # Set data
        cv2.putText(image, 'SETS: ' , (390, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, str(sets), (385,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        # Feedback data
        cv2.putText(image, 'FEEDBACK: ' , (560, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, feedback, (555,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                   mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()