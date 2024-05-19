import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def setha_angle(landmark1, landmark2):
    """각도 측정 함수"""
    a = np.array(landmark1)  # 첫 번째 점
    b = np.array(landmark2)  # 중간 점

    radians = np.arctan2(abs(a[0] - b[0]), abs(a[1] - b[1]))
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

def calculate_neck_score(left_shoulder_setha):
    """목 각도를 기반으로 점수를 반환하는 함수"""
    if left_shoulder_setha > 30:
        return 0
    elif left_shoulder_setha < 20:
        return 0
    elif 20 <= left_shoulder_setha < 23:
        return 100
    else:
        return 50

def analyze_neck_angle(image_path):
    """이미지 파일을 받아 목 각도를 분석하고 점수를 반환하는 함수"""
    # 이미지를 읽어오기
    image = cv2.imread(image_path)

    # Mediapipe Pose 인스턴스 초기화
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        # 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 이미지 처리
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # 주요 지점 추출
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            # 좌/우 몸 각도
            left_shoulder_setha = setha_angle(nose, left_shoulder)
            right_shoulder_setha = setha_angle(nose, right_shoulder)

            # 목 점수 계산
            neck_score = calculate_neck_score(left_shoulder_setha)

            # 각도 값을 화면에 출력
            cv2.putText(image, f"Neck Angle: {left_shoulder_setha:.1f} degrees",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # 목 점수 값을 화면에 출력
            cv2.putText(image, f"Neck Score: {neck_score}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 랜드마크 그리기
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # 결과 이미지 출력
        # cv2.imshow('Mediapipe Image Analysis', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return neck_score