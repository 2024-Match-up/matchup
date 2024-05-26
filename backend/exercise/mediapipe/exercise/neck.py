import numpy as np
import time
from logger import logger

class NeckExercise:
    def __init__(self):
        self.sets = 0
        self.counter = 0
        self.resting = False
        self.rest_start_time = 0
        self.Neck_angle = 0
        self.position = "Unknown"
        self.prev_position = "Ready"
        self.prev_time = time.time()

    def tri_calculate_angle(self, landmark1, landmark2, landmark3):
        try:
            vector1 = np.array(landmark1) - np.array(landmark2)
            vector2 = np.array(landmark3) - np.array(landmark2)
            dot_product = np.dot(vector1, vector2)
            magnitude_vector1 = np.linalg.norm(vector1)
            magnitude_vector2 = np.linalg.norm(vector2)
            cosine_angle = dot_product / (magnitude_vector1 * magnitude_vector2)
            angle_rad = np.arccos(cosine_angle)
            angle_deg = np.degrees(angle_rad)
            return angle_deg
        except Exception as e:
            logger.error(f"Error in tri_calculate_angle: {e}")
            return 0

    def vertical(self, x1, x2):
        try:
            threshold = abs(x1 - x2) * 0.3
            return abs(x1 - x2) <= threshold
        except Exception as e:
            logger.error(f"Error in vertical: {e}")
            return False

    def calculate_metrics(self, coordinates):
        try:
            coordinates = coordinates["coordinates"]
            nose = [coordinates[0]['dx'], coordinates[0]['dy']]
            left_eyes= [coordinates[1]['dx'], coordinates[1]['dy']]
            left_shoulder = [coordinates[2]['dx'], coordinates[2]['dy']]
            right_shoulder = [coordinates[3]['dx'], coordinates[3]['dy']]

            mid_shoulder = [(left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2]

            self.Neck_angle = self.tri_calculate_angle(left_shoulder, nose, right_shoulder)

            if left_shoulder[0] >= nose[0] >= right_shoulder[0]:
                self.position = "Ready"

            is_vertical_aligned = self.vertical(nose[0], mid_shoulder[0])
            if is_vertical_aligned and self.Neck_angle < 60:
                self.position = "Start"

            if self.Neck_angle < 50:
                self.position = "Stay"
                current_time = time.time()
                if current_time - self.prev_time >= 1:
                    self.counter += 1
                    self.prev_time = current_time
                    if self.counter > 10:
                        self.sets += 1
                        self.counter = 0
                        self.position = "Rest"
                        if self.position == "Rest":
                            time.sleep(3)

            return {
                'counter': self.counter,
                'sets': self.sets,
                'Neck_angle': self.Neck_angle,
                'position': self.position
            }
        except Exception as e:
            logger.error(f"Error in calculate_metrics: {e}")
            return {'error': str(e)}

    @staticmethod
    def get_neck_coordinates():
        coordinates = [
            "NOSE",
            "LEFT_EYE",
            "LEFT_SHOULDER",
            "RIGHT_SHOULDER"
        ]
        return coordinates
