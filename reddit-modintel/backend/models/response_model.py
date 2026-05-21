from pydantic import BaseModel
from typing import List


class TLDRResponse(BaseModel):
    one_liner: str
    bullets: List[str]
    tone: str


class SimilarityResult(BaseModel):
    index: int
    text: str
    score: float


class SimilarityResponse(BaseModel):
    results: List[SimilarityResult]