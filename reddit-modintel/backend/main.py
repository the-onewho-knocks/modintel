from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import tldr, similarity, analyze

load_dotenv()

app = FastAPI(title="ModIntel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tldr.router)
app.include_router(similarity.router)
app.include_router(analyze.router)


@app.get("/")
def root():
    return {"app": "ModIntel", "status": "ok"}