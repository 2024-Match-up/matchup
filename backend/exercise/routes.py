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

## Hardware 전용
@router.get("/{exercise_id}/{nickname}")
async def get_session_id(exercise_id: int, nickname: str, db: Session = Depends(get_db)):
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
    rc.set(f"{session_id}_hw_count", count)
    hw_set = int(rc.get(f"{session_id}_hw_set")) if rc.get(f"{session_id}_hw_set") is not None else 0

    if count < 10:
        return "keep"
    elif count >= 10 and hw_set < 2:
        hw_set += 1
        rc.set(f"{session_id}_hw_set", hw_set)
        return "set"
    else:
        if hw_set == 2:
            return "end"
    return {session_id, count}

@router.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("test1")
    await websocket.accept()

## 미디어 파이프 전용
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

        result_cnt = 0
        result_set = 0

        while True:
            data = await websocket.receive_text()
            if data:
                coordinates = json.loads(data)
                if "coordinates" not in coordinates or not coordinates["coordinates"]:
                    logger.error("Received empty coordinates data.")
                    continue

                exercise.write_exercise(coordinates)
                try:
                    metrics = exercise.calculate_metrics(coordinates=coordinates)
                except IndexError as e:
                    logger.error(f"Error in calculate_metrics: {e}")
                    continue

                hw_count = int(rc.get(f"{session_id}_hw_count")) if rc.get(f"{session_id}_hw_count") is not None else 0
                hw_set = int(rc.get(f"{session_id}_hw_set")) if rc.get(f"{session_id}_hw_set") is not None else 0
                prev_cnt = int(rc.get(f"{session_id}_mp_count")) if rc.get(f"{session_id}_mp_count") is not None else 0
                prev_set = int(rc.get(f"{session_id}_mp_set")) if rc.get(f"{session_id}_mp_set") is not None else 0

                cur_cnt = metrics.get('counter')
                cur_set = metrics.get('sets')

                logger.info(f"Previous count: {prev_cnt}, Current count: {cur_cnt}")
                logger.info(f"Previous set: {prev_set}, Current set: {cur_set}")
                logger.info(f"Hardware count: {hw_count}, Hardware set: {hw_set}")

                if cur_set != prev_set:
                    rc.set(f"{session_id}_mp_set", cur_set)
                    result_set = max(cur_set, prev_set)
                    logger.info(f"Set updated: {result_set}")

                if cur_cnt != prev_cnt or hw_count != prev_cnt:
                    rc.set(f"{session_id}_mp_count", cur_cnt)
                    result_cnt = max(hw_count, cur_cnt)
                    logger.info(f"Count updated: {result_cnt}")

                # 동기화 로직 추가
                if cur_cnt == 10 or hw_count == 10:
                    hw_count = 0
                    cur_cnt = 0
                    rc.set(f"{session_id}_hw_count", 0)
                    rc.set(f"{session_id}_mp_count", 0)
                    result_set += 1
                    rc.set(f"{session_id}_real_set", result_set)
                    logger.info(f"Set incremented: {result_set}")

                # 최종 카운트와 세트 저장
                rc.set(f"{session_id}_real_count", result_cnt)
                rc.set(f"{session_id}_real_set", result_set)

                logger.info(f"Final counts - result_cnt: {result_cnt}, result_set: {result_set}")

                # 비교 후 최종 카운트와 세트 전송
                metrics.update({'counter': result_cnt})
                metrics.update({'sets': result_set})

                logger.info(f"Sending metrics: {metrics}")
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

async def keep_websocket_alive(websocket: WebSocket):
    while True:
        await asyncio.sleep(10)
        try:
            await websocket.send_text("ping")
        except Exception as e:
            print("WebSocket connection error:", e)
