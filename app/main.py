from fastapi import FastAPI
from app.routers import services, deployments, users

app = FastAPI(
    title="DevOps Metrics API",
    description="API for tracking infrastructure deployment metrics",
    version="0.1.0",
)

app.include_router(services.router)
app.include_router(deployments.router)
app.include_router(users.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "DevOps Metrics API is running"}
