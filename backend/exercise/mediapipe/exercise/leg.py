import numpy as np
import time
from logger import logger
import csv
import datetime

class LegExercise:
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

        with open('leg.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["data"] + fieldnames)

            writer.writeheader()

            for group, entries in ex_data.items():
                for entry in entries:
                    row = {"data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    row.update(entry)
                    writer.writerow(row)

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def dou_calculate_angle(self, a, b):
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
            logger.error(f"Error in dou_calculate_angle: {e}")
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

            left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            hor_hip_angle = self.dou_calculate_angle(left_hip, right_hip)

            if (left_knee_angle > 160):
                self.position = "down"
            if (left_knee_angle < 100) and (self.position == 'down'):
                self.position = "up"
                self.counter += 1
                logger.info(f"횟수 : {self.counter}")
                if self.counter == 5:
                    self.sets += 1
                    self.counter = 0

            if (right_knee_angle > 160):
                self.position = "down"
            if (right_knee_angle < 100) and (self.position == 'down'):
                self.position = "up"
                self.counter += 1
                logger.info(f"횟수 : {self.counter}")
                if self.counter == 5:
                    self.sets += 1
                    self.counter = 0

            if hor_hip_angle < 10:
                self.feedback = "Good"
            else:
                self.feedback = "Bad"

            return {
                'counter': self.counter,
                'sets': self.sets,
                'feedback': self.feedback
            }
        except Exception as e:
            logger.error(f"Error in calculate_metrics: {e}")
            return {'error': str(e)}

    @staticmethod
    def get_lunge_coordinates():
        coordinates = [
            "LEFT_HIP",
            "RIGHT_HIP",
            "LEFT_KNEE",
            "RIGHT_KNEE",
            "LEFT_ANKLE",
            "RIGHT_ANKLE"
        ]
        return coordinates

if __name__ == "__main__":
    leg = LegExercise()
    for i in range(10):
        data = {'coordinates': [{'dx': 553.9432373046875, 'dy': 479.75146484375}, {'dx': 77.97301483154297, 'dy': 565.1355590820312}, {'dx': 780.8120727539062, 'dy': 748.90869140625}, {'dx': 86.8947525024414, 'dy': 874.7332153320312}]}
        leg.write_exercise(data)