from fastapi import FastAPI

app = FastAPI(
    title="DevOps Metrics API",
    description="API for tracking infrastructure deployment metrics",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "DevOps Metrics API is running"}
