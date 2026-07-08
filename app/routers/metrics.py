from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.db.database import get_db
from app.models.deployment import DeploymentModel
from app.models.service import ServiceModel
from app.schemas.metrics import MetricsSummary, ServiceMetrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricsSummary)
def get_metrics_summary(db: Session = Depends(get_db)):
    total_deployments = db.query(func.count(DeploymentModel.id)).scalar() or 0

    if total_deployments == 0:
        return MetricsSummary(
            total_deployments=0,
            overall_success_rate=0.0,
            by_service=[],
        )

    total_success = db.query(func.count(DeploymentModel.id)).filter(
        DeploymentModel.status == "success"
    ).scalar() or 0

    overall_success_rate = round((total_success / total_deployments) * 100, 2)

    per_service = (
        db.query(
            ServiceModel.id.label("service_id"),
            ServiceModel.name.label("service_name"),
            func.count(DeploymentModel.id).label("total_deployments"),
            func.avg(DeploymentModel.duration_seconds).label("avg_duration_seconds"),
            func.sum(
                case((DeploymentModel.status == "success", 1), else_=0)
            ).label("success_count"),
        )
        .join(DeploymentModel, DeploymentModel.service_id == ServiceModel.id)
        .group_by(ServiceModel.id, ServiceModel.name)
        .all()
    )

    by_service = [
        ServiceMetrics(
            service_id=row.service_id,
            service_name=row.service_name,
            total_deployments=row.total_deployments,
            success_rate=round((row.success_count / row.total_deployments) * 100, 2),
            avg_duration_seconds=round(float(row.avg_duration_seconds), 2),
        )
        for row in per_service
    ]

    return MetricsSummary(
        total_deployments=total_deployments,
        overall_success_rate=overall_success_rate,
        by_service=by_service,
    )
