# from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks, Depends
# from fastapi.responses import HTMLResponse
# from fastapi_another_jwt_auth import AuthJWT
# from template import html
# from logger import logger
# import json
# import asyncio
# from session.crud import create_session
# from session.schemas import Session
# from database import get_db
# from auth import AuthJWT
# from user.crud import authenticate_access_token, get_user
# from datetime import datetime, timezone
# import pytz # 한국 시간대로 설졍
# from exercise.mediapipe.exercise.waist import WaistExercise
# from exercise.mediapipe.exercise.squat import SquatExercise
# from exercise.mediapipe.exercise.leg import LegExercise
# from exercise.mediapipe.exercise.neck import NeckExercise

# # 한국 시간대
# kst = pytz.timezone('Asia/Seoul')

# router = APIRouter(
#     prefix="/api/v1/exercise",
#     tags=["exercise"],
# )

# # 운동을 시작하는 HTML 페이지를 반환하는 엔드포인트
# @router.get("/")
# async def get():
#     return HTMLResponse(html)

# @router.websocket("/test") # 웹소켓 연결을 처리하는 엔드포인트
# async def websocket_endpoint(websocket: WebSocket):
#     logger.info("test1")
#     await websocket.accept() # 클라이언트의 웬소켓 연결을 수락
    
# async def keep_websocket_alive(websocket: WebSocket):
#     while True:
#         await asyncio.sleep(10)  # 10초마다 웹 소켓 연결 확인
#         try:
#             await websocket.send_text("ping")  # 연결 확인을 위한 메시지 전송
#         except Exception as e:
#             # 연결이 끊어진 경우에는 다시 연결 시도 또는 새로운 연결 생성
#             # 이 부분을 웹 소켓 재연결 로직으로 수정하여 사용합니다.
#             print("WebSocket connection error:", e)

# @router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     background_tasks: BackgroundTasks,
#     Authorize: AuthJWT = Depends(),
#     db: Session = Depends(get_db),
# ):
#     await websocket.accept()
#     background_tasks.add_task(keep_websocket_alive, websocket)
    
#     try:
#         initial_data = await websocket.receive_text()
#         logger.info(f"Received initial data: {initial_data}")
#         initial_payload = json.loads(initial_data)
#         exercise_id = initial_payload.get("exercise_id")
#         access_token = initial_payload.get("access_token")

#         email = authenticate_access_token(access_token, Authorize)
#         logger.info(f"Authenticated user: {email}") 

#         user = get_user(db, email)
#         logger.info(f"User: {user}")
#         if user is None:
#             raise ValueError(f"User not found for email: {email}")
#         userId = user.id
#         logger.info(f"Authenticated user: {email} with userId: {userId}")

#         create_session(db, user_id=userId, exercise_id=exercise_id, date=datetime.now(kst))
#         await websocket.send_text(f"Session created for exercise ID: {exercise_id}")
#         logger.info(f"Session created for exercise ID: {exercise_id}")

#         if exercise_id == 1:
#             exercise = NeckExercise() # 목 운동을 위한 클래스 인스턴스 생성
#         elif exercise_id == 2:
#             exercise = SquatExercise()  # 스쿼트 운동을 위한 클래스 인스턴스 생성
#         elif exercise_id == 3:
#             exercise = LegExercise() # 다리 운동을 위한 클래스 인스턴스 생성
#         elif exercise_id == 4:
#             exercise = WaistExercise() # 허리 운동을 위한 클래스 인스턴스 생성
#         else:
#             await websocket.send_text("Invalid exercise ID")
#             await websocket.close()
#             return

#     except Exception as e:
#         logger.error(f"Authentication failed: {e}")
#         await websocket.send_text(f"Authentication failed: {e}")
#         await websocket.close()
#         return

#     try:
#         while True:
#             data = await websocket.receive_text()
#             coordinates = json.loads(data)
#             logger.info(f"Received coordinates: {coordinates}")

#             try:
#                 exercise.write_exercise(coordinates)
#                 metrics = exercise.calculate_metrics(coordinates=coordinates)
#                 logger.info(f"Metrics: {metrics}")
#                 await websocket.send_json(metrics)
#                 logger.info(f"Sent metrics: {metrics}")
#             except Exception as e:
#                 logger.error(f"Error calculating metrics: {e}")
#                 await websocket.send_json({'error': str(e)})

#     except WebSocketDisconnect:
#         logger.info("Client disconnected")
#     except Exception as e:
#         logger.error(f"Error during WebSocket communication: {e}")
#         await websocket.close()

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi_another_jwt_auth import AuthJWT
from template import html
from logger import logger
import json
import asyncio
from session.crud import create_session, get_latest_session_by_user_and_exercise
from models import Session 
from database import get_db
from auth import AuthJWT
from user.crud import authenticate_access_token, get_user, get_user_id_by_username
from datetime import datetime
import pytz
from exercise.mediapipe.exercise.waist import WaistExercise
from exercise.mediapipe.exercise.squat import SquatExercise
from exercise.mediapipe.exercise.leg import LegExercise
from exercise.mediapipe.exercise.neck import NeckExercise
import redis
import time

# redis_host = "127.0.0.1"
redis_host = "redis"
redis_port = 6379
redis_password = ""
rc = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

kst = pytz.timezone('Asia/Seoul')

router = APIRouter(
    prefix="/api/v1/exercise",
    tags=["exercise"],
)

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.get("/{exercise_id}/{nickname}")
async def get_session_id(exercise_id: int, nickname: str, db : Session = Depends(get_db)):
    userId = get_user_id_by_username(db, nickname)
    logger.info(f"User ID: {userId}")
    if not userId:
        raise HTTPException(status_code=404, detail="User not found")
    
    session = get_latest_session_by_user_and_exercise(db, exercise_id, userId)
    logger.info(f"Session: {session}")
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.id

@router.get("/count/{session_id}/{count}")
async def get_counts(session_id: int, count: int):
    rc.set(f"{session_id}_hw_count" , count)
    temp_count = int(rc.get(f"{session_id}_hw_count"))
    print(type(temp_count))
    temp_set = rc.get(f"{session_id}_hw_set")
    if temp_set is None:
        temp_set = 0
    else:
        temp_set = int(temp_set)
    if temp_count < 10:
        return "keep"
    elif temp_count >= 10 and temp_set < 2 :
        temp_set += 1
        rc.set(f"{session_id}_hw_set", temp_set)
        return "set"
    else:
        if temp_set == 2 :
            return "end"
    return {session_id, count}

@router.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("test1")
    await websocket.accept()

async def keep_websocket_alive(websocket: WebSocket):
    while True:
        await asyncio.sleep(10)
        try:
            await websocket.send_text("ping")
        except Exception as e:
            print("WebSocket connection error:", e)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    background_tasks: BackgroundTasks,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    await websocket.accept()
    background_tasks.add_task(keep_websocket_alive, websocket)
    
    try:
        initial_data = await websocket.receive_text()
        logger.info(f"Received initial data: {initial_data}")
        initial_payload = json.loads(initial_data)
        exercise_id = initial_payload.get("exercise_id")
        access_token = initial_payload.get("access_token")
        
        email = authenticate_access_token(access_token, Authorize)
        user = get_user(db, email)
        userId = user.id
        session = create_session(db, user_id=userId, exercise_id=exercise_id, date=datetime.now(kst))
        session_id = session.id
        
        await websocket.send_text(f"Session created for exercise ID: {exercise_id}, Session ID: {session_id}")
        
        exercise = create_exercise_instance(exercise_id)

        while True:
            data = await websocket.receive_text()
            coordinates = json.loads(data)
            hw_count = int(rc.get(f"{session_id}_hw_count") or 0)
            mp_count = int(rc.get(f"{session_id}_mp_count") or 0)
            
            exercise.write_exercise(coordinates)
            metrics = exercise.calculate_metrics(coordinates=coordinates)
            real_count = max(hw_count, mp_count) 
            
            if hw_count > 0 or mp_count > 0:
                real_count += 1
                rc.set(f"{session_id}_real_count", real_count)
                rc.set(f"{session_id}_hw_count", 0) 
                rc.set(f"{session_id}_mp_count", 0)  
            
            metrics.update({'real_count': real_count})
            await websocket.send_json(metrics)

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error during WebSocket communication: {e}")
        await websocket.close()

def create_exercise_instance(exercise_id):
    if exercise_id == 1:
        return NeckExercise()
    elif exercise_id == 2:
        return SquatExercise() 
    elif exercise_id == 3:
        return LegExercise()
    elif exercise_id == 4:
        return WaistExercise()
    else:
        raise ValueError("Invalid exercise ID")
