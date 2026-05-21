from fastapi import APIRouter, HTTPException
from models.request_model import TLDRRequest
from models.response_model import TLDRResponse
from services.tldr_service import generate_tldr

router = APIRouter()


@router.post("/tldr", response_model=TLDRResponse)
def tldr(req: TLDRRequest):
    word_count = len(req.text.split())
    if word_count <= 200:
        raise HTTPException(
            status_code=400,
            detail=f"Post must have more than 200 words (got {word_count})"
        )
    try:
        result = generate_tldr(req.text)
        return TLDRResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))