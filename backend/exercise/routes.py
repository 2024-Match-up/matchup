from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, HTTPException
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from template import html
from logger import logger
import json
import asyncio
from session.crud import create_session, get_latest_session_by_user_and_exercise
from database import get_db
from user.crud import authenticate_access_token, get_user, get_user_id_by_username
from datetime import datetime
import pytz
from exercise.mediapipe.exercise.waist import WaistExercise
from exercise.mediapipe.exercise.squat import SquatExercise
from exercise.mediapipe.exercise.leg import LegExercise
from exercise.mediapipe.exercise.neck import NeckExercise
import redis
import models
from typing import List
from exercise.schemas import SessionScore, FinalScoreResponse

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

@router.get("/scores/{exercise_id}", summary="운동 아이디별 점수와 날짜 조회", response_model=List[SessionScore])
async def get_scores_by_exercise_id(
    exercise_id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Received request to get scores for exercise ID: {exercise_id}")

    # JWT 토큰 인증
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    logger.info(f"Authenticated user: {current_user}")

    email = authenticate_access_token(current_user, Authorize=Authorize)
    logger.info(f"User email extracted from token: {email}")

    user = get_user(db, email)
    if not user:
        logger.error(f"User not found for email: {email}")
        raise HTTPException(status_code=400, detail="User not found.")

    # 세션 데이터 조회
    logger.info(f"Querying sessions for exercise ID: {exercise_id}")
    sessions = db.query(models.Session).filter(models.Session.exercise_id == exercise_id).all()
    if not sessions:
        logger.error(f"No sessions found for exercise ID: {exercise_id}")
        raise HTTPException(status_code=404, detail="No sessions found for the given exercise_id")

    # 결과 데이터 생성
    result = [SessionScore(date=session.date, score=session.score if session.score is not None else 0) for session in sessions]
    logger.info(f"Returning {len(result)} sessions for exercise ID: {exercise_id}")

    return result

# 최종 점수 조회 엔드포인트 수정
@router.get("/session/{session_id:int}/final_score", summary="최종 점수 조회", response_model=FinalScoreResponse)
async def get_final_score(
    session_id: int, 
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    logger.info(f"Received request to get final score for session ID: {session_id}")

    # JWT 토큰 인증
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    logger.info(f"Authenticated user: {current_user}")

    email = authenticate_access_token(current_user, Authorize=Authorize)
    logger.info(f"User email extracted from token: {email}")

    user = get_user(db, email)
    if not user:
        logger.error(f"User not found for email: {email}")
        raise HTTPException(status_code=400, detail="User not found.")

    # 세션 데이터베이스에서 최종 점수 가져오기
    logger.info(f"Querying session for session ID: {session_id} and user ID: {user.id}")
    session = db.query(models.Session).filter(models.Session.id == session_id, models.Session.user_id == user.id).first()

    if not session or session.score is None:
        logger.error(f"Final score not found for session ID: {session_id}")
        raise HTTPException(status_code=404, detail="Final score not found.")

    final_score = session.score
    logger.info(f"Returning final score for session ID: {session_id}: {final_score}")
    return FinalScoreResponse(session_id=session_id, final_score=final_score)

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

                # 점수 계산 및 저장
                total_count = rc.get(f"{session_id}_total_count") or 0
                total_count = int(total_count) + 1

                hw_weight = 0.6
                mp_weight = 0.4

                # 가중치 차이 계산
                count_difference = abs(hw_count - cur_cnt)
                max_difference = 10  # 최대 차이를 설정
                weighted_difference = (count_difference / max_difference) * 100  # 백분율로 변환

                # 점수를 백분율로 계산
                final_score = max(0, 100 - weighted_difference)

                if total_count >= 30:
                    rc.set(f"{session_id}_final_score", final_score)
                    session.score = final_score  # DB에 점수 저장
                    db.commit()
                    logger.info(f"Final Score: {final_score}%")
                    await websocket.send_text(f"Final Score: {final_score}%")
                    await websocket.close()
                    break

                rc.set(f"{session_id}_total_count", total_count)

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
            logger.error("WebSocket connection error:", e)


