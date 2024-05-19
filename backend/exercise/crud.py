# from fastapi import WebSocket
# import asyncio
# import numpy as np
# from logger import logger
# import cv2
# import base64
# import json
# import mediapipe as mp
# from mediapipe.python.solutions import pose as mp_pose
# from mediapipe.python.solutions import drawing_utils as mp_drawing
# from mediapipe.python.solutions import drawing_styles as mp_drawing_styles


# mp_pose = mp.solutions.pose

# async def send_detection_results(websocket: WebSocket):
#     cap = cv2.VideoCapture(0) // 파이썬에서 로컬기기에서 카메라를 켜는 기기
#     with mp_pose.Pose(
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5,
#             model_complexity=1) as pose:
#         i = 0
#         while cap.isOpened():
#             i += 1
#             success, image = cap.read()
#             if not success:
#                 logger.info("카메라를 찾을 수 없습니다.")
#                 continue
#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             results = pose.process(image)

#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             mp_drawing.draw_landmarks(
#                 image,
#                 results.pose_landmarks,
#                 mp_pose.POSE_CONNECTIONS,
#                 landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#             img = cv2.flip(image, 1)
#             _, buffer = cv2.imencode('.jpg', img)
#             frame_bytes = buffer.tobytes()
#             frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')
#             message = json.dumps({'frame': frame_base64, 'message': f"counter: {i}"})
#             await websocket.send_text(message)
#             await asyncio.sleep(0.1)
#     cap.release()