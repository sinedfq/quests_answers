from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session

from schemas.schemas import CreateQuestion
from services.questions_service import delete_question_by_id, add_question, get_question_and_answers, get_all_questions

router = APIRouter(tags=["Вопросы"])

@router.get(
    "/questions/",
    summary="Список всех вопросов"
)
async def get_questions(session: AsyncSession = Depends(get_session)):
    return await get_all_questions(session)

@router.get(
    "/questions/{question_id}",
    summary="Получить вопрос и все ответы на него")
async def get_question_answers(
        question_id: int,
        session: AsyncSession = Depends(get_session)
):
    return await get_question_and_answers(question_id, session)

@router.post(
    "/questions/",
    summary="Создать новый вопрос"
)
async def create_question(new_question: CreateQuestion,
                          session: AsyncSession = Depends(get_session)
                          ):
    question = await add_question(new_question, session)
    return {"status": "success", "question": question}


@router.delete(
    "/questions/{id}",
    summary="Удалить вопрос и ответы к нему"
)
async def delete_question(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    deleted_id = await delete_question_by_id(id, session)
    return {"status": "success", "question": deleted_id}
