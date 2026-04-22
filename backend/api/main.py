from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import predict, simulate, countries

app = FastAPI(
    title="War Prediction & Conflict Simulator API",
    description="ML-powered conflict prediction and war simulation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(simulate.router)
app.include_router(countries.router)


@app.get("/")
async def root():
    return {
        "message": "War Prediction & Conflict Simulator API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)