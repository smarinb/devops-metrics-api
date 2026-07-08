from pydantic import BaseModel


class ServiceMetrics(BaseModel):
    service_id: int
    service_name: str
    total_deployments: int
    success_rate: float
    avg_duration_seconds: float


class MetricsSummary(BaseModel):
    total_deployments: int
    overall_success_rate: float
    by_service: list[ServiceMetrics]
