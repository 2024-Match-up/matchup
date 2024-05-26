import csv

def write_leg(ex_data):
    with open('leg.csv', 'w', newline='') as csvfile:
        fieldnames = ["left_hip_x", "left_hip_y", "right_hip_x", "right_hip_y", "left_knee_x", "left_knee_y", "right_knee_x", "right_knee_y", "left_ankle_x", "left_ankle_y", "right_ankle_x", "right_ankle_y"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(ex_data)

def write_neck(ex_data):
    with open('neck.csv', 'w', newline='') as csvfile:
        fieldnames = ["nose_x", "nose_y", "left_eye_x", "left_eye_y", "left_shoulder_x", "left_shoulder_y", "right_shoulder_x", "right_shoulder_y"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(ex_data)

def write_squat(ex_data):
    with open('squat.csv', 'w', newline='') as csvfile:
        fieldnames = ["left_hip_x", "left_hip_y", "right_hip_x", "right_hip_y", "left_knee_x", "left_knee_y", "right_knee_x", "right_knee_y", "left_ankle_x", "left_ankle_y", "right_ankle_x", "right_ankle_y"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(ex_data)

def write_waist(ex_data):
    with open('waist.csv', 'w', newline='') as csvfile:
        fieldnames = ["left_shoulder_x", "left_shoulder_y", "right_shoulder_x", "right_shoulder_y", "left_elbow_x", "left_elbow_y", "right_elbow_x", "right_elbow_y"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(ex_data)