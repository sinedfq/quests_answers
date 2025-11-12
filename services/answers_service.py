from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Question, Answer
from schemas.schemas import CreateAnswer

async def get_answer_by_id(answer_id: int, session: AsyncSession):
    result = await session.execute(select(Answer).where(Answer.id == answer_id))
    answer = result.scalar_one_or_none()
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ с таким ID не найден")
    return {
        "answer": {
            "id": answer.id,
            "question_id": answer.question_id,
            "text": answer.text,
            "user_id": answer.user_id
        }
    }

async def add_new_answer(question_id: int,
                         new_answer: CreateAnswer,
                         session: AsyncSession):
    result = await session.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    existing = await session.execute(
        select(Answer).where(
            Answer.question_id == question_id,
            Answer.user_id == new_answer.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже ответил на этот вопрос")

    answer = Answer(
        question_id = question_id,
        text = new_answer.text,
        user_id = new_answer.user_id
    )
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return {"status": "success", "answer": answer}

async def delete_answer_by_id(id: int,session: AsyncSession):
    result = await session.execute(select(Answer).where(Answer.id == id))
    answer = result.scalar_one_or_none()
    if not answer:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    await session.delete(answer)
    await session.commit()

    return {"status": "success", "answer_id": id}