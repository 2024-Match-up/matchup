import numpy as np
import time
from logger import logger
import csv

class WaistExercise:
    def __init__(self):
        # 상태 변수 초기화
        self.sets = 0
        self.counter = 0
        self.resting = False
        self.rest_start_time = 0
        self.left_arm_raised = False
        self.right_arm_raised = False
        self.feedback = None
        self.last_position = "None"
    
    def write_exercise(self, ex_data):
        fieldnames = set()
        for key in ex_data:
            for entry in ex_data[key]:
                fieldnames.update(entry.keys())

        fieldnames = list(fieldnames)

        # Write data to CSV
        with open('waist.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["data"] + fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data rows
            for group, entries in ex_data.items():
                for entry in entries:
                    row = {"data": group}
                    row.update(entry)
                    writer.writerow(row)

    def dou_calculate_angle(self, a, b):
        try:
            a = np.array(a)
            b = np.array(b)
            logger.info(f"a: {a}, b: {b}")  # 디버깅 로그 추가
            horizontal_vector = np.array([1, 0])
            ab_vector = abs(b - a)
            logger.info(f"ab_vector: {ab_vector}")  # 디버깅 로그 추가
            radians = np.arccos(
                np.dot(ab_vector, horizontal_vector) / (np.linalg.norm(ab_vector) * np.linalg.norm(horizontal_vector))
            )
            logger.info(f"radians: {radians}")  # 디버깅 로그 추가
            angle = np.abs(radians * 180.0 / np.pi)
            logger.info(f"angle: {angle}")  # 디버깅 로그 추가
            return angle
        except Exception as e:
            logger.error(f"Error in dou_calculate_angle: {e}")
            return 0

    def calculate_metrics(self, coordinates):
        try:
            logger.info(f"Received 우어어ㅓcoordinates: {coordinates}")  # 디버깅 로그 추가
            coordinates = coordinates["coordinates"]
            left_shoulder = [coordinates[0]['dx'], coordinates[0]['dy']]
            right_shoulder = [coordinates[1]['dx'], coordinates[1]['dy']]
            left_elbow = [coordinates[2]['dx'], coordinates[2]['dy']]
            right_elbow = [coordinates[3]['dx'], coordinates[3]['dy']]

            logger.info(f"left_shoulder: {left_shoulder}, right_shoulder: {right_shoulder}, left_elbow: {left_elbow}, right_elbow: {right_elbow}")  # 디버깅 로그 추가

            hor_shoulder_angle = self.dou_calculate_angle(left_shoulder, right_shoulder)
            hor_elbow_angle = self.dou_calculate_angle(left_elbow, right_elbow)

            left_arm_angle = self.dou_calculate_angle(left_shoulder, left_elbow)
            right_arm_angle = self.dou_calculate_angle(right_shoulder, right_elbow)

            position = "None"

            if not self.resting:
                # Ready 상태: 양 팔꿈치가 어깨보다 위에 있고 수평 유지
                if left_shoulder[1] > left_elbow[1] and right_shoulder[1] > right_elbow[1]:
                    if hor_shoulder_angle <= 5 and hor_elbow_angle <= 5:
                        position = "Ready"
                        if self.right_arm_raised and self.left_arm_raised and self.last_position == "Ready":
                            self.counter += 1
                            logger.info(f"횟수 : {self.counter}")
                            self.left_arm_raised = False
                            self.right_arm_raised = False
                            if self.counter >= 10:
                                self.sets += 1
                                self.counter = 0
                                position = "Rest"
                                self.resting = True
                                self.rest_start_time = time.time()
                        self.last_position = "Ready"
                # 왼쪽 팔꿈치가 어깨보다 낮고 팔 각도가 특정 임계값 초과
                if left_elbow[1] > left_shoulder[1] and left_arm_angle > 30:
                    position = "Left"
                    self.left_arm_raised = True
                    self.last_position = "Left"

                # 오른쪽 팔꿈치가 어깨보다 낮고 팔 각도가 특정 임계값 초과
                if right_elbow[1] > right_shoulder[1] and right_arm_angle > 30:
                    position = "Right"
                    self.right_arm_raised = True
                    self.last_position = "Right"
            else:
                elapsed_time = time.time() - self.rest_start_time
                if elapsed_time >= 10:
                    self.resting = False
                    position = "Ready"
                else:
                    position = f"Rest: {int(10 - elapsed_time)}s"
                self.last_position = "Rest"

            if hor_shoulder_angle < 40 and hor_shoulder_angle >= 30:
                self.feedback = "어깨가 너무 낮습니다."
            elif hor_shoulder_angle >= 40 and hor_shoulder_angle < 55:
                self.feedback = "자세가 좋습니다."
            elif hor_shoulder_angle > 55:
                self.feedback = "어깨가 너무 높습니다."

            return {
                'counter': self.counter,
                'sets': self.sets,
                'feedback': self.feedback
            }
        except Exception as e:
            logger.error(f"Error in calculate_metrics: {e}")
            return {'error': str(e)}


    def get_waist_coordinates():
        coordinates = [
            "LEFT_SHOULDER",
            "RIGHT_SHOULDER",
            "LEFT_ELBOW",
            "RIGHT_ELBOW"
        ]
        return coordinates
