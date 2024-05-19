import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 점수
score_shoulder = 0
score_hip = 0
score_leg = 0
# 참고 자료 : https://kwonkai.tistory.com/141
def tri_calculate_angle(landmark1, landmark2, landmark3):
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
# 두 점의 각도
def dou_calculate_angle(landmark1, landmark2):
    a = np.array(landmark1)
    b = np.array(landmark2)

    # 수평 벡터 계산
    horizontal_vector = np.array([1, 0])

    # 두 점 사이의 벡터 계산
    ab_vector = abs(b - a)

    # 두 벡터 사이의 각도 계산
    radians = np.arccos(
        np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector)))
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

#  각도 측정
def setha_angle(landmark1, landmark2):
    a = np.array(landmark1)  # 첫 번째 점
    b = np.array(landmark2)  # 중간 점

    radians2 = np.arctan2(abs(a[0] - b[0]), abs(a[1] - b[1]))
    angle2 = np.abs(radians2 * 180.0 / np.pi)

    return angle2


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
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                             landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # 좌/우 몸 각도
            left_shoulder_setha = setha_angle(nose, left_shoulder)
            left_hip_setha = setha_angle(left_shoulder, left_hip)
            left_ankle_setha = setha_angle(left_hip, left_ankle)
            right_shoulder_setha = setha_angle(nose, right_shoulder)
            right_hip_setha = setha_angle(right_shoulder, right_hip)
            right_ankle_setha = setha_angle(right_hip, right_ankle)

            # 골반 : 골반과 무릎, 발목 : 무릎 사이각
            left_angle = tri_calculate_angle(left_hip, left_knee, left_ankle)
            right_angle = tri_calculate_angle(right_hip, right_knee, right_ankle)


            # 전면부 : 골반 기울기
            hor_shoulder_angle = dou_calculate_angle(left_shoulder, right_shoulder)
            hor_hip_angle = dou_calculate_angle(left_hip, right_hip)



            #좌표 리스트
            # 코, 좌/우 어깨, 골반, 무릎 발목
            # 수평 어깨, 골반, 왼쪽다리 오른쪽다리
            list_All = [nose, left_shoulder, left_hip, left_ankle, left_knee, right_shoulder, right_hip, right_ankle,left_knee,
                        hor_shoulder_angle, hor_hip_angle, left_angle, right_angle]
            # 점수 확인
            # 점수는 어깨, 골반, 다리 확인
            # 어깨 : 멀어지면 수평을 잘 인식 못해서 5점부터 시작
            if hor_shoulder_angle < 5:
                score_shoulder = 50
            elif hor_shoulder_angle < 2:
                score_shoulder = 100
            else:
                score_shoulder = 0

            # 골반 : 멀어지면 수평을 잘 인식 못해서 5점부터 시작
            if hor_hip_angle < 5:
                score_hip = 50
            elif hor_hip_angle < 2:
                score_hip = 100
            else :
                score_hip = 0

            # 다리 : 좌/우 값이 다르나, 평균을 냄
            if left_angle < 175 or right_angle < 175:
                score_leg = 50
            elif 175 <= (left_angle or right_angle) <= 180:
                score_leg = 100
            else :
                score_leg = 0
            # 각도 값을 화면에 출력
            cv2.putText(image, f"Shoulder Angle: {hor_shoulder_angle:.1f} degrees",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Hip Angle: {hor_hip_angle:.1f} degrees",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"leg Angle: {left_angle:.1f} degrees",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 각도 화면에 띄우기
            cv2.putText(image, f"{hor_shoulder_angle:.3f}",
                        tuple(np.multiply(left_shoulder, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"{hor_hip_angle:.3f}",
                        tuple(np.multiply(left_hip, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"{left_knee[0]:.3f}",
                        tuple(np.multiply(left_angle, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

            '''# 좌표 확인
            for i in range(len(list_ALL)):
                print(f"해당 좌표 : {i} ", list_ALL[i])'''




            # 랜드마크 그리기
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))


        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
