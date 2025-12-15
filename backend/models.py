
from sqlalchemy import Column, Integer, String, Text
from backend.database import Base
from pydantic import BaseModel
from typing import List

class QuestionAnswer(Base):
    __tablename__ = "questions_answers"
    id = Column(Integer, primary_key=True, index=True)
    question_title = Column(String(512), nullable=False)
    question_body = Column(Text, nullable=True)
    answer_body = Column(Text, nullable=True)
    tags = Column(String(256), nullable=True)
    url = Column(String(512), nullable=True)


# Pydantic schema for API responses
class QuestionAnswerSchema(BaseModel):
    id: int
    question_title: str
    question_body: str = None
    answer_body: str = None
    tags: str = None
    url: str = None

    class Config:
        orm_mode = True


class AIResponse(BaseModel):
    answer: str
    sources: List[int]  # list of IDs referencing QuestionAnswer entries
```

```plaintext
