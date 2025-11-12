from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key = True, index = True)
    text = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False, default = func.now())

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key = True, index = True)
    question_id = Column(Integer, ForeignKey("questions.id"), index = True)
    user_id = Column(String, nullable = False)
    text = Column(String, nullable = False)
    created_at = Column(DateTime, nullable = False, default = func.now())

    question = relationship("Question", back_populates="answers")


DATABASE_URL = "postgresql+asyncpg://postgres:1234@db/question_answer"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False )


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session