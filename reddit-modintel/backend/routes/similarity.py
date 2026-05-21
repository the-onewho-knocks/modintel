from fastapi import APIRouter, HTTPException
from models.request_model import SimilarityRequest
from models.response_model import SimilarityResponse, SimilarityResult
from services.plagiarism_service import check_similarity

router = APIRouter()


@router.post("/similarity", response_model=SimilarityResponse)
def similarity(req: SimilarityRequest):
    try:
        results = check_similarity(req.target, req.corpus)
        return SimilarityResponse(
            results=[SimilarityResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))