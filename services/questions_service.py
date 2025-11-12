from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Question, Answer
from schemas.schemas import CreateQuestion

async def delete_question_by_id(question_id: int, session: AsyncSession):
    fetch_data = await session.execute(select(Question).where(Question.id == question_id))
    question = fetch_data.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    await session.execute(delete(Question).where(Question.id == question_id))
    await session.commit()

    return question_id

async def add_question(new_question: CreateQuestion,
                          session: AsyncSession):
    question = Question(
        text = new_question.text
    )
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question

async def get_question_and_answers(question_id: int,
                                   session: AsyncSession):
    stmt = select(Question, Answer).outerjoin(Answer, Question.id == Answer.question_id).where(Question.id == question_id)
    result = await session.execute(stmt)
    rows = result.all()

    if not rows:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    question = rows[0][0]
    answers = [row[1] for row in rows if row[1] is not None]

    return {
        "question": {
            "id": question.id,
            "text": question.text
        },
        "answers": [{"id": a.id, "text": a.text, "user_id": a.user_id} for a in answers]
    }

async def get_all_questions(session: AsyncSession):
    result = await session.execute(select(Question))
    questions = result.scalars().all()
    if not questions:
        raise HTTPException(status_code = 404, detail= "Вопрос не найден")
    return questions