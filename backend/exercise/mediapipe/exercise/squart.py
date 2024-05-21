# import cv2
# import mediapipe as mp
# import numpy as np

# # Initialize mediapipe
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# cap = cv2.VideoCapture(0)

# # Calculate the angle between three points
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
    
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
    
#     if angle > 180.0:
#         angle = 360 - angle
        
#     return angle

# # Calculate the horizontal angle between two points
# def calculate_horizontal_angle(a, b):
#     a = np.array(a)
#     b = np.array(b)
#     horizontal_vector = np.array([1, 0])
#     ab_vector = abs(b - a)
    
#     radians = np.arccos(
#         np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector))
#     )
#     angle = np.abs(radians * 180.0 / np.pi)

#     return angle

# # Draw text on the image
# def draw_text(image, text, position):
#     cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

# # Draw status box on the image
# def draw_status_box(image, counter, position, sets, feedback):
#     cv2.rectangle(image, (0, 0), (700, 73), (245, 117, 16), -1)

#     draw_text(image, 'REPS: ', (20, 20))
#     draw_text(image, str(counter), (15, 60))

#     draw_text(image, 'POSITION: ', (190, 20))
#     draw_text(image, position, (185, 60))

#     draw_text(image, 'SETS: ', (390, 20))
#     draw_text(image, str(sets), (385, 60))

#     draw_text(image, 'FEEDBACK: ', (560, 20))
#     draw_text(image, feedback, (555, 60))

# # Extract landmarks and calculate necessary angles
# def process_landmarks(landmarks):
#     left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                      landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#     left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
#                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
#     left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
#                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
#     left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
#                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

#     right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
#                       landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
#     right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
#                  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
#     right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
#                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
#     right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
#                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

#     left_angle = calculate_angle(left_hip, left_knee, left_ankle)
#     right_angle = calculate_angle(right_hip, right_knee, right_ankle)
#     horizontal_hip_angle = calculate_horizontal_angle(left_hip, right_hip)

#     return left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_angle, right_angle, horizontal_hip_angle

# # Main function to start exercise session
# def start_exercise_session():
#     counter = 0
#     sets = 0
#     feedback = None
#     position = None

#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             frame = cv2.flip(frame, 1)
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False

#             results = pose.process(image)

#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             if results.pose_landmarks:
#                 landmarks = results.pose_landmarks.landmark
#                 (
#                     left_shoulder, right_shoulder, left_hip, right_hip,
#                     left_knee, right_knee, left_ankle, right_ankle,
#                     left_angle, right_angle, horizontal_hip_angle
#                 ) = process_landmarks(landmarks)

#                 cv2.putText(image, str(left_angle),
#                             tuple(np.multiply(left_knee, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(image, str(right_angle),
#                             tuple(np.multiply(right_knee, [640, 480]).astype(int)),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#                 if (left_angle > 160) and (right_angle > 160):
#                     position = "down"
#                 if (left_angle < 100) and (right_angle < 100) and (position == 'down'):
#                     position = "up"
#                     counter += 1
#                     print("Counter:", counter)
#                     if counter == 10:
#                         sets += 1
#                         counter = 0

#                 feedback = "Good" if horizontal_hip_angle < 10 else "Bad"

#                 list_all = [left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, feedback]
#                 print(list_all)

#             draw_status_box(image, counter, position, sets, feedback)
#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                       mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                       mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

#             cv2.imshow('Mediapipe Feed', image)

#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     start_exercise_session()

import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# Calculate the horizontal angle between two points
def calculate_horizontal_angle(a, b):
    a = np.array(a)
    b = np.array(b)
    horizontal_vector = np.array([1, 0])
    ab_vector = abs(b - a)
    
    radians = np.arccos(
        np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector))
    )
    angle = np.abs(radians * 180.0 / np.pi)

    return angle

# Draw text on the image
def draw_text(image, text, position):
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

# Draw status box on the image
def draw_status_box(image, counter, position, sets, feedback):
    cv2.rectangle(image, (0, 0), (700, 73), (245, 117, 16), -1)

    draw_text(image, 'REPS: ', (20, 20))
    draw_text(image, str(counter), (15, 60))

    draw_text(image, 'POSITION: ', (190, 20))
    draw_text(image, position, (185, 60))

    draw_text(image, 'SETS: ', (390, 20))
    draw_text(image, str(sets), (385, 60))

    draw_text(image, 'FEEDBACK: ', (560, 20))
    draw_text(image, feedback, (555, 60))

# Extract landmarks and calculate necessary angles
def process_landmarks(landmarks):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    left_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_angle = calculate_angle(right_hip, right_knee, right_ankle)
    horizontal_hip_angle = calculate_horizontal_angle(left_hip, right_hip)

    return left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_angle, right_angle, horizontal_hip_angle

# Function to return joint points for hip exercise
def get_hip_joint_points(landmarks):
    left_shoulder, right_shoulder, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_angle, right_angle, horizontal_hip_angle = process_landmarks(landmarks)
    
    joint_points = {
        "left_shoulder": left_shoulder,
        "right_shoulder": right_shoulder,
        "left_hip": left_hip,
        "right_hip": right_hip,
        "left_knee": left_knee,
        "right_knee": right_knee,
        "left_ankle": left_ankle,
        "right_ankle": right_ankle,
        "left_angle": left_angle,
        "right_angle": right_angle,
        "horizontal_hip_angle": horizontal_hip_angle
    }
    return joint_points

# Main function to start exercise session
def start_exercise_session():
    counter = 0
    sets = 0
    feedback = None
    position = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                joint_points = get_hip_joint_points(landmarks)
                
                left_angle = joint_points["left_angle"]
                right_angle = joint_points["right_angle"]
                horizontal_hip_angle = joint_points["horizontal_hip_angle"]
                
                cv2.putText(image, str(left_angle),
                            tuple(np.multiply(joint_points["left_knee"], [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(right_angle),
                            tuple(np.multiply(joint_points["right_knee"], [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                if (left_angle > 160) and (right_angle > 160):
                    position = "down"
                if (left_angle < 100) and (right_angle < 100) and (position == 'down'):
                    position = "up"
                    counter += 1
                    print("Counter:", counter)
                    if counter == 10:
                        sets += 1
                        counter = 0

                feedback = "Good" if horizontal_hip_angle < 10 else "Bad"

            draw_status_box(image, counter, position, sets, feedback)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_exercise_session()
