import numpy as np
import time
from logger import logger
import csv

class SquatExercise:
    def __init__(self):
        self.sets = 0
        self.counter = 0
        self.resting = False
        self.rest_start_time = 0
        self.position = None
        self.feedback = None

    def write_exercise(self, ex_data):
        fieldnames = set()
        for key in ex_data:
            for entry in ex_data[key]:
                fieldnames.update(entry.keys())

        fieldnames = list(fieldnames)

        # Write data to CSV
        with open('squat.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["data"] + fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data rows
            for group, entries in ex_data.items():
                for entry in entries:
                    row = {"data": group}
                    row.update(entry)
                    writer.writerow(row)

    def calculate_angle(self, a, b, c):
        try:
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            if angle > 180.0:
                angle = 360 - angle
            return angle
        except Exception as e:
            logger.error(f"Error in calculate_angle: {e}")
            return 0

    def calculate_horizontal_angle(self, a, b):
        try:
            a = np.array(a)
            b = np.array(b)
            horizontal_vector = np.array([1, 0])
            ab_vector = abs(b - a)
            radians = np.arccos(
                np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector))
            )
            angle = np.abs(radians * 180.0 / np.pi)
            return angle
        except Exception as e:
            logger.error(f"Error in calculate_horizontal_angle: {e}")
            return 0

    def calculate_metrics(self, coordinates):
        try:
            logger.info(f"Received coordinates: {coordinates}")
            coordinates = coordinates["coordinates"]
            left_hip = [coordinates[0]['dx'], coordinates[0]['dy']]
            right_hip = [coordinates[1]['dx'], coordinates[1]['dy']]
            left_knee = [coordinates[2]['dx'], coordinates[2]['dy']]
            right_knee = [coordinates[3]['dx'], coordinates[3]['dy']]
            left_ankle = [coordinates[4]['dx'], coordinates[4]['dy']]
            right_ankle = [coordinates[5]['dx'], coordinates[5]['dy']]

            left_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            right_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            horizontal_hip_angle = self.calculate_horizontal_angle(left_hip, right_hip)

            if (left_angle > 160) and (right_angle > 160):
                self.position = "down"
            if (left_angle < 100) and (right_angle < 100) and (self.position == 'down'):
                self.position = "up"
                self.counter += 1
                logger.info(f"횟수: {self.counter}")
                if self.counter == 10:
                    self.sets += 1
                    self.counter = 0

            self.feedback = "자세가 좋습니다." if horizontal_hip_angle < 10 else "허리를 펴주세요."

            return {
                'counter': self.counter,
                'sets': self.sets,
                'feedback': self.feedback
            }
        except Exception as e:
            logger.error(f"Error in calculate_metrics: {e}")
            return {'error': str(e)}

    def get_squat_coordinates():
        coordinates = [
            "LEFT_HIP",
            "RIGHT_HIP",
            "LEFT_KNEE",
            "RIGHT_KNEE",
            "LEFT_ANKLE",
            "RIGHT_ANKLE"
        ]
        return coordinates
