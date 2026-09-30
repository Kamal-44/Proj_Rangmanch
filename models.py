from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
# from  pytz import timezone

class Reviews(SQLModel,table=True):
    # table = true means this a table, create a table for this
    id:Optional[int] =Field(default=None,primary_key=True) #integer based optional field
    play_name:str =Field(index=True)    # searching things it can be searced with help of play_name, index helps in filtering
    reviewer_name:str
    rating: int=Field(ge=1,le=5) # ge= greater than or equal to 1, le=less than equal to 5
    comment: str
    # created_at:datetime=Field(default_factory=datetime.now(timezone('UTC')))
   # default factory will directly store this and save time based on creation time of record



class ReviewCreate(SQLModel):
    play_name:str
    reviewer_name:str
    rating:int =Field(ge=1,le=5)
    comment:str

class ReadReview(SQLModel):
    id:int
    play_name:str
    reviewer_name:str
    rating:int =Field(ge=1,le=5)
    comment:str
    # created_at:datetime

class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(ge=1, le=5)
    comment: Optional[str] = None