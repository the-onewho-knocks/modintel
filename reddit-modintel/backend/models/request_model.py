from pydantic import BaseModel , Field
from typing import List

class TLDRRequest(BaseModel):
    text : str = Field(... , min_length=1 , description="Post content to summarize")

class SimilarityRequest(BaseModel):
    target: str = Field(... , min_length=1 , description="Text to check against corpus")
    corpus: List[str] = Field(... , min_length= 1 , description="List of texts to compare againts")