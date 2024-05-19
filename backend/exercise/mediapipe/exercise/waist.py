import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


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


# 변수 초기화
sets = 0
counter = 0
count = 0

position = "Unknown"
prev_position = "Unknown"

current_time = 0
prev_time = 0

resting = False
rest_start_time = 0

# 왼쪽 팔과 오른쪽 팔의 움직임을 추적하는 플래그 초기화
left_arm_raised = False
right_arm_raised = False

feedback = None


# 웹캠 비디오 캡처
cap = cv2.VideoCapture(0)

# Mediapipe Pose 인스턴스 초기화
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("프레임 읽기 오류")
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark


            # 주요 지점 추출
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            # 수평
            hor_shoulder_angle = dou_calculate_angle(left_shoulder, right_shoulder)
            hor_elbow_angle = dou_calculate_angle(left_elbow, right_elbow)

            # 팔 각도
            left_arm = dou_calculate_angle(left_shoulder, left_elbow)
            right_arm = dou_calculate_angle(right_shoulder, right_elbow)

            list_All = [left_shoulder, left_elbow, right_shoulder, right_elbow,
                        left_arm, right_arm, hor_shoulder_angle, hor_elbow_angle
                        , feedback]

            if not resting:
                # 기본1 : 양 팔꿈치가 어깨보다 위에 있으면서
                if left_shoulder[1] > left_elbow[1] and right_shoulder[1] > right_elbow[1]:
                    # 수평 상태(5도 미만)
                    if hor_shoulder_angle <= 5 and hor_elbow_angle <= 5:
                        position = "Ready"
                        # 기본 2 : 좌 / 우 모두 한 번씩 했다면
                        if (right_arm_raised == True) and (left_arm_raised == True):
                            position = "Go"
                            counter += 1
                            print("횟수 : ", counter)
                            left_arm_raised = False
                            right_arm_raised = False
                            if counter >= 10:
                                sets += 1
                                counter = 0
                                position = "Rest"
                                resting = True
                                rest_start_time = time.time()
                # 왼쪽 아래로 : 왼쪽 팔꿈치가 어깨보다 낮으면서 팔의 각도는 50 이상
                if left_elbow[1] > left_shoulder[1] and left_arm > 30 and hor_shoulder_angle > 30:
                    position = "Left"
                    left_arm_raised = True

                    # 오른쪽 아래로 : 오른쪽 팔꿈치가 어깨보다 낮으면서 팔의 각도는 50 이상
                if right_elbow[1] > right_shoulder[1] and right_arm > 30 and hor_shoulder_angle > 30:
                    position = "Right"
                    right_arm_raised = True

            else:
                elapsed_time = time.time() - rest_start_time
                if elapsed_time >= 10:
                    resting = False
                    position = "Ready"
                else:
                    position = f"Rest: {int(2 - elapsed_time)}s"

            # 점수
            if hor_shoulder_angle < 40 and hor_shoulder_angle >= 30:
                feedback = "It's too low"
            elif hor_shoulder_angle >= 40 and hor_shoulder_angle < 55:
                feedback = "normal"
            elif hor_shoulder_angle > 55:
                feedback = "Good"

            # Setup status box
            cv2.rectangle(image, (0,0), (700,73), (245,117,16), -1)
             
            # Rep data
            cv2.putText(image, 'REPS: ' , (20, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(counter), (15,60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'POSITION: ' , (230, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, position, (225,60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            # Set data
            cv2.putText(image, 'SETS: ' , (450, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, str(sets), (445,60), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


            # 각도 화면에 띄우기
            cv2.putText(image, f"{hor_elbow_angle:.3f}",
                        tuple(np.multiply((left_elbow[0] + right_elbow[0] / 2), [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

            # 랜드마크 그리기
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()