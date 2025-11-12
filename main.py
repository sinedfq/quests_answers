import uvicorn
from fastapi import FastAPI
from routers.questions import router as questions_router
from routers.answers import router as answers_router

app = FastAPI(title="Questions")
app.include_router(questions_router)
app.include_router(answers_router)

@app.get("/")
async def root():
    return {"message": "Questions API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)