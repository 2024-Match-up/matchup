import mediapipe as mp
import numpy as np
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def setha_angle(landmark1, landmark2):
    """Calculate angle between two points."""
    a = np.array(landmark1)  # First point
    b = np.array(landmark2)  # Second point

    radians = np.arctan2(abs(a[0] - b[0]), abs(a[1] - b[1]))
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

def calculate_neck_score(left_shoulder_setha):
    """Return score based on neck angle."""
    if left_shoulder_setha > 30:
        return 0
    elif left_shoulder_setha < 20:
        return 0
    elif 20 <= left_shoulder_setha < 23:
        return 100
    else:
        return 50

def analyze_neck_angle(image_path):
    """Analyze neck angle from an image file and return the score."""
    image = cv2.imread(image_path)
    # image_path = 'backend/health/측면.png'
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return None
    
    image = cv2.resize(image, (640, 480))

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        

        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_shoulder_setha = setha_angle(nose, left_shoulder)
            right_shoulder_setha = setha_angle(nose, right_shoulder)

            print(f"Left Shoulder Angle: {left_shoulder_setha:.1f} degrees")
            print(f"Right Shoulder Angle: {right_shoulder_setha:.1f} degrees")

            score_neck = calculate_neck_score(left_shoulder_setha)

            """
            # 없어도 되는 코드(확인용)
            cv2.putText(image, f"Neck Angle: {left_shoulder_setha:.1f} degrees",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(image, f"Neck Score: {score_neck}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
            cv2.imshow('Mediapipe Image Analysis', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """

        else:
            print("No pose landmarks detected")
            return None
        return_score = {"neck": score_neck}
        return return_score


# image_path = 'backend/exercise/mediapipe/측면.jpeg'  
# neck_score = analyze_neck_angle(image_path)

# if neck_score is not None:
#     print(f"Neck Score: {neck_score}")
# else:
#     print("Neck landmarks were not detected.")