from pydantic import BaseModel, Field, ConfigDict

class CreateQuestion(BaseModel):
    text: str = Field(min_length = 1)

    model_config = ConfigDict(extra='forbid')

class CreateAnswer(BaseModel):
    text: str = Field(min_length = 1)
    user_id: str = Field(min_length = 1)

    model_config = ConfigDict(extra='forbid')