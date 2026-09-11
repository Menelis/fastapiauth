from pydantic import BaseModel, Field, ConfigDict

class BookCreate(BaseModel):
    title:str = Field(min_length=1, max_length=50)
    author:str = Field(min_length=1, max_length=50)
    
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str
    author:str