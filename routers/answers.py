from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from schemas.schemas import CreateAnswer
from services.answers_service import get_answer_by_id, add_new_answer, delete_answer_by_id

router = APIRouter(tags=["Ответы"])

@router.get(
    "/answers/{id}",
    summary="Получить конкретный ответ"
)
async def get_answer(id: int, session: AsyncSession = Depends(get_session)):
    return await get_answer_by_id(id, session)


@router.post(
    "/questions/{id}/answers/",
    summary="Добавить ответ к вопросу"
)
async def add_answer(id: int,
                     new_answer: CreateAnswer,
                     session: AsyncSession = Depends(get_session),
                     ):
    return await add_new_answer(id, new_answer, session)

@router.delete(
    "/answers/{id}",
    summary="Удалить ответ"
)
async def delete_answer(id: int,
                        session: AsyncSession = Depends(get_session)):
    return await delete_answer_by_id(id, session)