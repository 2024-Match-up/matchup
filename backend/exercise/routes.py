from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
# from auth import AuthJWT
from fastapi.responses import HTMLResponse
from template import html
from .crud import send_detection_results
from datetime import datetime
import json
from models import Exercise, Session as ExerciseSession
from logger import logger
from database import get_db


router = APIRouter(
    prefix="/api/v1/exercise",
    tags=["exercise"],
)

# 요청을 받으면 html 내용을 HTML 응답으로 반환한다. 
@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws") # 웹소켓 연결을 처리하는 엔드포인트
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # 클라이언트의 웬소켓 연결을 수락
    await send_detection_results(websocket) 
    # 실시간으로 데이터를 주고받는 기능을 수행하는 함수로, 웹소켓 객체를 인수로 받아 데이터를 처리 


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Exercise WebSocket</title>
    </head>
    <body>
        <h1>Exercise WebSocket</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/exercise/ws/5");  // 세션 ID를 적절히 수정
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            ws.onclose = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode("WebSocket connection closed")
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var data = JSON.stringify({
                    coordinates: [1, 2, 3, 4],
                    count: parseInt(input.value)
                });
                ws.send(data)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.post("/start-exercise/{exercise_id}/{user_id}")
async def start_exercise(exercise_id: int, user_id: int, db: Session = Depends(get_db)):
    # 운동 정보를 가져오기
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # 세션 생성 및 DB에 저장
    session = ExerciseSession(
        user_id=user_id,
        exercise_id=exercise_id,
        date=datetime.now(),
        status="not_started",
        coordinates=exercise.coordinate_list
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {"session_id": session.id, "status": session.status, "coordinates": session.coordinates}

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, db: Session = Depends(get_db)):
    await websocket.accept()

    session = db.query(ExerciseSession).filter(ExerciseSession.id == session_id).first()
    if not session:
        await websocket.close(code=1003)
        return

    session.status = "ongoing"
    db.commit()

    try:
        while True:
            try:
                data = await websocket.receive_text()
                data = json.loads(data)
                
                coordinates = data.get("coordinates", [])
                count = data.get("count")

                if count is None:
                    raise ValueError("Count value is missing")

                # 실시간 피드백 계산
                feedback = "Good" if count % 2 == 0 else "Bad"  # 예시 피드백 로직
                session.feedback = feedback
                session.real_count = count
                db.commit()

                response = {
                    "coordinates": coordinates,
                    "count": count,
                    "feedback": feedback
                }
                await websocket.send_text(json.dumps(response))
            except json.JSONDecodeError as e:
                await websocket.send_text(json.dumps({"error": "Invalid JSON format", "details": str(e)}))
            except ValueError as e:
                await websocket.send_text(json.dumps({"error": "Value error", "details": str(e)}))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": "Error processing message", "details": str(e)}))

    except WebSocketDisconnect:
        session.status = "disconnected"
        db.commit()
