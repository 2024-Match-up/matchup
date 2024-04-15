from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/")
async def signup():
    return {"message": "회원가입"}