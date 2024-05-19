import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def tri_calculate_angle(landmark1, landmark2, landmark3):
    """Calculate angle between three points."""
    vector1 = np.array(landmark1) - np.array(landmark2)
    vector2 = np.array(landmark3) - np.array(landmark2)
    dot_product = np.dot(vector1, vector2)
    magnitude_vector1 = np.linalg.norm(vector1)
    magnitude_vector2 = np.linalg.norm(vector2)
    cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)
    angle_rad = np.arccos(cosine_angle)
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def dou_calculate_angle(landmark1, landmark2):
    """Calculate horizontal angle between two points."""
    a = np.array(landmark1)
    b = np.array(landmark2)
    horizontal_vector = np.array([1, 0])
    ab_vector = abs(b - a)
    radians = np.arccos(
        np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector)))
    angle = np.abs(radians * 180.0 / np.pi)
    return angle

def setha_angle(landmark1, landmark2):
    """Calculate angle between two points."""
    a = np.array(landmark1)
    b = np.array(landmark2)
    radians2 = np.arctan2(abs(a[0] - b[0]), abs(a[1] - b[1]))
    angle2 = np.abs(radians2 * 180.0 / np.pi)
    return angle2

def calculate_scores(landmarks):
    """Calculate scores based on landmarks."""
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

    left_shoulder_setha = setha_angle(nose, left_shoulder)
    left_hip_setha = setha_angle(left_shoulder, left_hip)
    left_ankle_setha = setha_angle(left_hip, left_ankle)
    right_shoulder_setha = setha_angle(nose, right_shoulder)
    right_hip_setha = setha_angle(right_shoulder, right_hip)
    right_ankle_setha = setha_angle(right_hip, right_ankle)

    left_angle = tri_calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = tri_calculate_angle(right_hip, right_knee, right_ankle)

    hor_shoulder_angle = dou_calculate_angle(left_shoulder, right_shoulder)
    hor_hip_angle = dou_calculate_angle(left_hip, right_hip)

    score_shoulder = 0
    score_hip = 0
    score_leg = 0

    if hor_shoulder_angle < 5:
        score_shoulder = 50
    elif hor_shoulder_angle < 2:
        score_shoulder = 100
    else:
        score_shoulder = 0

    if hor_hip_angle < 5:
        score_hip = 50
    elif hor_hip_angle < 2:
        score_hip = 100
    else:
        score_hip = 0

    if left_angle < 175 or right_angle < 175:
        score_leg = 50
    elif 175 <= (left_angle or right_angle) <= 180:
        score_leg = 100
    else:
        score_leg = 0

    return score_shoulder, score_hip, score_leg

def process_image(image_path):
    """Process image and return scores."""
    # image_path = 'backend/health/정면.png'
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return None, None, None

    # Resize the image for faster processing
    image = cv2.resize(image, (640, 480))

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            score_shoulder, score_hip, score_leg = calculate_scores(landmarks)

            # 없어도 되는 코드(확인용)
            # Optionally draw landmarks on the image (commented out for speed)
            # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            #                           mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            #                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
            # cv2.imshow('Mediapipe Feed', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            return_dict = dict()
            return_dict = {
                "waist": score_shoulder,
                "pelvis": score_hip,
                "leg": score_leg
            }
            return return_dict
        else:
            print("No pose landmarks detected")
            return None, None, None

# # Test
# image_path = 'backend/exercise/mediapipe/정면.jpeg' 
# shoulder_score, hip_score, leg_score = process_image(image_path)
# if shoulder_score is not None:
#     print(f"Shoulder Score: {shoulder_score}, Hip Score: {hip_score}, Leg Score: {leg_score}")
