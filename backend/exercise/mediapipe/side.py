import cv2
import mediapipe as mp
import numpy as np
import math as m

# 수직 기준 각도 계산 함수
def Angle(landmark1, landmark2):
    a = np.array(landmark1)
    b = np.array(landmark2)
    c = (a[0], a[1] - 100)

    # 벡터 BA와 BC를 계산합니다.
    BA = (a[0] - b[0], a[1] - b[1])
    BC = (c[0] - b[0], c[1] - b[1])

    # 벡터 BA와 BC의 내적을 계산합니다.
    dot_product = BA[0] * BC[0] + BA[1] * BC[1]

    # 벡터 BA와 BC의 크기를 계산합니다.
    magnitude_BA = m.sqrt(BA[0] ** 2 + BA[1] ** 2)
    magnitude_BC = m.sqrt(BC[0] ** 2 + BC[1] ** 2)

    # 두 벡터의 내적과 크기를 이용하여 라디안 각도를 계산합니다.
    angle_radians = m.acos(dot_product / (magnitude_BA * magnitude_BC))
    # 라디안 각도를 도로 변환하여 반환합니다.
    angle_degrees = angle_radians * (180 / m.pi)
    return angle_degrees

# 목 점수 계산 함수
def calculate_neck_score(neck_inclination):
    """Return score based on neck angle."""
    if neck_inclination < 40:
        score = int(80 - (neck_inclination / 40 * 80) + 20)
        position = "Good"
    else:
        score = 20
        position = "Bad"
    return score, position

# mediapipe 자세 클래스 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def analyze_neck_angle(image_path):
    """Analyze neck angle from an image file and return the score."""
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return None
    
    image = cv2.resize(image, (640, 480))

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w = image.shape[:2]

        left_shoulder = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h))

        left_ear = (int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].x * w),
                    int(landmarks[mp_pose.PoseLandmark.LEFT_EAR].y * h))

        neck_inclination = Angle(left_shoulder, left_ear)

        print(f"Neck Inclination Angle: {neck_inclination:.1f} degrees")

        score_neck, position = calculate_neck_score(neck_inclination)
    else:
        print("No pose landmarks detected")
        return None

    return score_neck


image_path = 'backend/exercise/mediapipe/측면1.jpeg'  
neck_score_측면1 = analyze_neck_angle(image_path)
neck_score_측면2 = analyze_neck_angle(image_path)

if neck_score_측면1 is not None:
    print(f"Neck Score: {neck_score_측면1}")
else:
    print("Neck landmarks were not detected.")

if neck_score_측면2 is not None:
    print(f"Neck Score: {neck_score_측면2}")
else:
    print("Neck landmarks were not detected.")