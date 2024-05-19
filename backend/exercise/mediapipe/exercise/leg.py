import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 변수 초기화
sets = 0
counter = 0
feedback = None
prev_position = "Ready"

current_time = 0

prev_time = 0

# 세 점 사이의 각도를 계산하는 함수 정의
def calculate_angle(landmark1, landmark2, landmark3):
    # 두 벡터 계산
    vector1 = np.array(landmark1) - np.array(landmark2)
    vector2 = np.array(landmark3) - np.array(landmark2)

    # 벡터의 내적 계산
    dot_product = np.dot(vector1, vector2)

    # 벡터의 크기 계산
    magnitude_vector1 = np.linalg.norm(vector1)
    magnitude_vector2 = np.linalg.norm(vector2)

    # 코사인 값 계산
    cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)

    # 각도 계산
    angle_rad = np.arccos(cosine_angle)
    angle_deg = np.degrees(angle_rad)

    return angle_deg
# 수평 계산 : 수평이면 0도여야하기에 180 - angle
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
# 웹캠에서 비디오를 캡처하기 위한 VideoCapture 객체를 생성합니다.
cap = cv2.VideoCapture(0)

# Mediapipe 인스턴스 설정
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    position = "Unknown" # 초기화

    while cap.isOpened():
        ret, frame = cap.read()

        # 이미지 색상 변환 (BGR -> RGB)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 감지 수행
        results = pose.process(image)

        # 이미지 색상 변환 (RGB -> BGR)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 랜드마크 추출
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

           
            # 살짝 기댄다고 가정 : 어깨, 골반, 발목
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            hor_left_leg_angle = dou_calculate_angle(left_hip, left_ankle)
            hor_right_leg_angle = dou_calculate_angle(right_hip, right_ankle)

            # 무릎과 발목으로 기울기 잡으니까 자꾸 이상하게 나와서 그냥 어깨, 골반, 발목으로 잡음


            position1 = "Ready"
            position2 = "Ready"


            left_leg_angle = calculate_angle(left_shoulder, left_hip, left_ankle)
            if left_leg_angle >= 115 and hor_left_leg_angle < 40:
                position1 = "LEFT_UP"
            if left_leg_angle <= 115:
                position1 = "LEFT_Stay"
                current_time = time.time()
                if current_time - prev_time >= 1:
                    counter += 1
                    prev_time = current_time
                    print("Counter:", counter)
                    if counter >= 10:  # 5초 버티기
                        sets += 1
                        counter = 0
                        # 휴식시간 코드
                        position1 = "Rest"
                        if position1 == "Rest":
                            time.sleep(3)

            right_leg_angle = calculate_angle(right_shoulder, right_hip, right_ankle)
                # 앉는 자세
            if right_leg_angle >= 115 and hor_right_leg_angle < 40:
                position2 = "RIGHT_UP"

            if right_leg_angle <= 115:
                position2 = "RIGHT_Stay"
                current_time = time.time()
                if current_time - prev_time >= 1:
                    counter += 1
                    prev_time = current_time
                    print("Counter:", counter)
                    if counter >= 10:  # 5초 버티기
                        sets += 1
                        counter = 0
                        # 휴식시간 코드
                        position2 = "Rest"
                        if position2 == "Rest":
                            time.sleep(3)

            if right_leg_angle > 115 or left_leg_angle > 115:
                feedback = "Bad"
            elif  80 < left_leg_angle < 115 or 80 < left_leg_angle < 115:
                feedback = "Good"
            
            
            
            
            list_ALL = [
                        left_shoulder, right_shoulder, left_ankle, right_ankle, left_leg_angle, right_leg_angle, feedback]

            # 화면에 표시
            # Setup status box
            cv2.rectangle(image, (0,0), (700,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(image, 'REPS: ' , (20, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(counter), (15,60),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'POSITION: ' , (130, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, position1, (130, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, position2, (270, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


            # Set data
            cv2.putText(image, 'SETS: ' , (450, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(sets), (445,60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Feedback data
            cv2.putText(image, 'FEEDBACK: ' , (560, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, feedback, (555,60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


        # 감지된 랜드마크 그리기
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()