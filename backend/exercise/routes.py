from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
import pytz
import redis
import models  # 데이터베이스 모델 임포트
from models import Session as SessionModel  # 데이터베이스 모델의 Session 클래스 임포트
from session.crud import create_session, get_latest_session_by_user_and_exercise
from user.crud import authenticate_access_token, get_user, get_user_id_by_username
from exercise.schemas import SessionScore, FinalScoreResponse
from logger import logger
from template import html
import json
import asyncio
from typing import List
from exercise.mediapipe.exercise.waist import WaistExercise
from exercise.mediapipe.exercise.squat import SquatExercise
from exercise.mediapipe.exercise.leg import LegExercise
from exercise.mediapipe.exercise.neck import NeckExercise
from database import get_db
import csv
import datetime as dt
from datetime import datetime

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

@router.get("/scores", response_model=List[SessionScore])
async def get_all_scores(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_email = authenticate_access_token(current_user, Authorize=Authorize)
    user = get_user(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    sessions = db.query(SessionModel).filter(SessionModel.user_id == user.id).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found")

    return [
        SessionScore(
            date=session.date.isoformat(),  # ISO 포맷으로 날짜를 문자열로 변환
            score=session.score if session.score is not None else 0,
            exercise_id=session.exercise_id  # exercise_id 제공 확인
        ) for session in sessions
    ]

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
    session = db.query(SessionModel).filter(SessionModel.id == session_id, SessionModel.user_id == user.id).first()

    if not session or session.score is None:
        logger.error(f"Final score not found for session ID: {session_id}")
        raise HTTPException(status_code=404, detail="Final score not found.")

    final_score = session.score
    logger.info(f"Returning final score for session ID: {session_id}: {final_score}")
    return FinalScoreResponse(session_id=session_id, final_score=final_score)

## Hardware 전용
@router.get("/{exercise_id}/user/{nickname}", summary="닉네임과 운동 아이디로 세션 ID 조회")
async def get_session_id_by_nickname(exercise_id: int, nickname: str, db: Session = Depends(get_db)):
    logger.info(f"Received request to get session ID for exercise ID: {exercise_id} and nickname: {nickname}")

    user_id = get_user_id_by_username(db, nickname)
    logger.info(f"User ID: {user_id}")
    if not user_id:
        logger.error(f"User not found for nickname: {nickname}")
        raise HTTPException(status_code=404, detail="User not found")

    session = get_latest_session_by_user_and_exercise(db, user_id, exercise_id)
    logger.info(f"Session: {session}")
    if not session:
        logger.error(f"Session not found for exercise ID: {exercise_id} and user ID: {user_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    return session.id

# @router.get("/session/{session_id}/count/{count}/hw", summary="HW 카운트 갱신")
# async def get_counts(session_id: int, count: int):
#     # rc.set(f"{session_id}_hw_count", count)
#     hw_set = int(rc.get(f"{session_id}_hw_set")) if rc.get(f"{session_id}_hw_set") is not None else 0

#     if count < 5:
#         rc.set(f"{session_id}_hw_count", count)
#         return "keep"
#     elif count >= 5 and hw_set < 2:
#         hw_set += 1
#         rc.set(f"{session_id}_hw_set", hw_set)
#         return "set"
#     else:
#         if hw_set == 2:
#             rc.set(f"{session_id}_hw_count", count)
#             return "end"
#     return {session_id, count}


def write_exercise(ex_data):
    fieldnames = set()
    for key in ex_data:
        for entry in ex_data[key]:
            fieldnames.update(entry.keys())

    fieldnames = list(fieldnames)

    with open('hw_squat.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["data"] + fieldnames)

        writer.writeheader()

        for group, entries in ex_data.items():
            for entry in entries:
                row = {"data": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                row.update(entry)
                writer.writerow(row)

@router.get("/session/{session_id}/count/{count}/hw", summary="HW 카운트 갱신")
async def get_counts(session_id: int, count: int):
    hw_set = int(rc.get(f"{session_id}_hw_set")) if rc.get(f"{session_id}_hw_set") is not None else 0

    if count < 5:
        rc.set(f"{session_id}_hw_count", count)
        status = "keep"
    elif count >= 5 and hw_set < 2:
        hw_set += 1
        rc.set(f"{session_id}_hw_set", hw_set)
        status = "set"
    else:
        if hw_set == 2:
            rc.set(f"{session_id}_hw_count", count)
            status = "end"
    
    # 기록할 데이터 준비
    ex_data = {
        session_id: [{"count": count, "status": status}]
    }
    write_exercise(ex_data)

    return status


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
        session = create_session(db, user_id=userId, exercise_id=exercise_id, date=dt.datetime.now(kst))
        session_id = session.id

        await websocket.send_text(f"Session created for exercise ID: {exercise_id}, Session ID: {session_id}")

        exercise = create_exercise_instance(exercise_id)

        result_cnt = 0
        result_set = 0
        final_score = 0

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

                hw_count = int(rc.get(f"{session_id}_hw_count") or 0)
                hw_set = int(rc.get(f"{session_id}_hw_set") or 0)
                mp_cnt = int(rc.get(f"{session_id}_mp_count") or 0)
                mp_set = int(rc.get(f"{session_id}_mp_set") or 0)

                cur_mp_cnt = metrics.get('counter', 0)
                cur_mp_set = metrics.get('sets', 0)

                logger.info(f"Previous count: {mp_cnt}, Current count: {cur_mp_cnt}")
                logger.info(f"Previous set: {mp_set}, Current set: {cur_mp_set}")
                logger.info(f"Hardware count: {hw_count}, Hardware set: {hw_set}")
                
                # 세트와 카운트 값이 변경되었을 때만 업데이트
                if cur_mp_set != mp_set:
                    rc.set(f"{session_id}_mp_set", cur_mp_set)
                    result_set = max(cur_mp_set, mp_set)
                    result_cnt = 0  
                    logger.info(f"Set updated: {result_set}")

                ## 카운트 값이 변경되었을 때만 업데이트
                if cur_mp_cnt != mp_cnt:
                    if result_set > 0:
                        result_cnt = 0
                    rc.set(f"{session_id}_mp_count", cur_mp_cnt)
                    result_cnt = max(mp_cnt, cur_mp_cnt)
                    logger.info(f"Count updated: {result_cnt}")

                result_cnt = max(cur_mp_cnt, hw_count)
                result_set = max(cur_mp_set, hw_set)

                # 점수 계산 및 저장
                total_count = 5 * result_set + result_cnt if result_cnt != 5 else 5 * result_set
                hw_weight = 0.7
                mp_weight = 0.3

                # 점수를 백분율로 계산
                # final_score = 20 * (cur_mp_cnt * mp_weight + hw_count * hw_weight)
                # logger.info(f"Final Score: {final_score}%")
                
                # 점수를 백분율로 계산
                def get_final_score(cur_mp_cnt, hw_count, exercise_id):
                    if exercise_id == 1 or exercise_id == 4:
                        return 20 * cur_mp_cnt
                    elif exercise_id == 2 or exercise_id == 3:
                        return 20 * (cur_mp_cnt * mp_weight + hw_count * hw_weight)
                
                # 기존 코드    
                # final_score = 20 * (cur_mp_cnt * mp_weight + hw_count * hw_weight)
                
                # 변경된 코드
                final_score = get_final_score(cur_mp_cnt, hw_count, exercise_id)

                if result_set == 0 and result_cnt == 4:
                    rc.set(f"{session_id}_final_score", final_score)
                    session.score = final_score  # DB에 점수 저장
                    db.commit()
                    logger.info(f"Final Score: {final_score}%, Total Count: {total_count}")
                    await websocket.send_json({"final_score": final_score, "total_count": total_count})
                    # await websocket.close()
                    break
                else :
                    logger.info(f"Final counts - result_cnt: {result_cnt}, result_set: {result_set}")

                    # 비교 후 최종 카운트와 세트 전송
                    if(result_cnt != 5):
                        metrics.update({'counter': result_cnt})
                        metrics.update({'sets': result_set})
                    else:
                        metrics.update({'counter': 0})
                        metrics.update({'sets': result_set})
                    
                    logger.info(f"Sending metrics: {metrics}")
                    await websocket.send_json(metrics)
        await websocket.close()

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
