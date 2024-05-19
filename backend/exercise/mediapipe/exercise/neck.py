import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 변수 초기화
sets = 0
counter = 0

position = "Unknown"
prev_position = "Unknown"

current_time = 0
prev_time = 0

feedback = None

#  각도 측정
def setha_angle(landmark1, landmark2):
    a = np.array(landmark1)  # 첫 번째 점
    b = np.array(landmark2)  # 중간 점

    radians2 = np.arctan2(abs(a[0] - b[0]), abs(a[1] - b[1]))
    angle2 = np.abs(radians2 * 180.0 / np.pi)

    return angle2

def vertical(landmark1, landmark2, landmark3):
    x1, x2, x3 = landmark1[0], landmark2[0], landmark3[0]
    average_x = (x1 + x2 + x3) / 3
    threshold = average_x * 0.05

    if (abs(x1 - average_x) <= threshold) and (abs(x2 - average_x) <= threshold) and (abs(x3 - average_x) <= threshold):
        return True
    else:
        return False

# 웹캠에서 비디오를 캡처하기 위한 VideoCapture 객체를 생성합니다.
cap = cv2.VideoCapture(0)

# Mediapipe 인스턴스 설정
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
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

            # 정자세 -> 일정한 각도 : 어깨, 골반, 발목
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value] if landmarks else None

            if nose:  # nose가 None이 아닌 경우에만 실행
                nose = [nose.x, nose.y]

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                left_shoulder_setha = setha_angle(nose, left_shoulder)
                left_hip_setha = setha_angle(left_shoulder, left_hip)
                left_ankle_setha = setha_angle(left_hip, left_ankle)

                right_shoulder_setha = setha_angle(nose, right_shoulder)
                right_hip_setha = setha_angle(right_shoulder, right_hip)
                right_ankle_setha = setha_angle(right_hip,right_ankle)


            # 1. 정자세로 서있는것 : 어깨, 골반, 발목에 대한 평균에서 5% 내외에 들어가게
            # 수직 여부 확인
            left_vertical = vertical(left_shoulder, left_hip, left_ankle)
            right_vertical = vertical(right_shoulder, right_hip, right_ankle)

            # 결과 표기
            if left_vertical:
                position = "Ready"

            # 정자세 : if left_hip_setha > 5 and left_ankle_setha > 5 and left_shoulder_setha < 10:
            if left_hip_setha > 5 and left_ankle_setha > 5:
                position = "Stay"
                current_time = time.time()
                if current_time - prev_time >= 1:
                    counter += 1
                    prev_time = current_time
                    print("Counter:", counter)
                    if counter == 5: # 5초 버티기
                        sets += 1
                        counter = 0
                        # 휴식시간 코드
                        position = "Rest"
                        time.sleep(10)  # 10초

            # 결과 표기
            if right_vertical:
               position = "Ready"

            # 정자세 : if left_hip_setha > 5 and left_ankle_setha > 5 and left_shoulder_setha < 10:
            if right_hip_setha > 5 and right_ankle_setha > 5:
                position = "Stay"
                current_time = time.time()
                if current_time - prev_time >= 1:
                    counter += 1
                    prev_time = current_time
                    print("Counter:", counter)
                    if counter == 5:  # 5초 버티기
                        sets += 1
                        counter = 0
                        # 휴식시간 코드 : Rest 뜨는 동안 counter 늘어나지 않는지 확인하고, sets 고정되는지도 확인
                        position = "Rest"
                        time.sleep(10)  # 10초

            list_All = [nose, left_shoulder, left_hip, left_ankle, right_shoulder, right_hip, right_ankle,
                        left_shoulder_setha, left_hip_setha, left_ankle_setha, right_shoulder_setha,
                        right_hip_setha, right_ankle_setha, left_vertical, right_vertical,
                        feedback]


            # 상태 표기
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

            # 점수
            if (5< right_hip_setha <= 8) and (5 < right_ankle_setha) and \
                    (5 < left_hip_setha <= 8) and (5< left_ankle_setha):
                feedback = "Tilting more"
            elif (8 < right_hip_setha <= 15) and (8 < right_ankle_setha) and \
                    (8 < left_hip_setha <= 15) and (8 < left_ankle_setha):
                feedback = "normal"
            elif (15 < right_hip_setha <= 30) and (8 < right_ankle_setha) and \
                    (15 < left_hip_setha <= 30) and (8 < left_ankle_setha):
                feedback = "Good"
            else :
                feedback = "Error"

                    # 감지된 랜드마크 그리기
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()