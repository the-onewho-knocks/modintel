from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from services.tldr_service import generate_tldr
from services.plagiarism_service import check_similarity

router = APIRouter()


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Post content to analyze")
    corpus: List[str] = Field(
        default_factory=list,
        description="Corpus for similarity check (optional)"
    )


class AnalyzeTLDR(BaseModel):
    one_liner: str
    bullets: List[str]
    tone: str


class AnalyzeSimilarityResult(BaseModel):
    index: int
    text: str
    score: float


class AnalyzeResponse(BaseModel):
    tldr: AnalyzeTLDR | None = None
    similarity: List[AnalyzeSimilarityResult] | None = None
    tldr_skipped: bool = False
    similarity_skipped: bool = False


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    resp = AnalyzeResponse()

    word_count = len(req.text.split())
    if word_count > 200:
        try:
            tldr_result = generate_tldr(req.text)
            resp.tldr = AnalyzeTLDR(**tldr_result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"TLDR failed: {e}")
    else:
        resp.tldr_skipped = True

    if req.corpus:
        try:
            results = check_similarity(req.text, req.corpus)
            resp.similarity = [AnalyzeSimilarityResult(**r) for r in results]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Similarity failed: {e}")
    else:
        resp.similarity_skipped = True

    return resp