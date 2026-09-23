from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from backend.models.api import Api
from backend.models.asset import Asset


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self):
        total_assets = self.db.query(Asset).count()
        total_apis = self.db.query(Api).count()

        assets_by_provider = (
            self.db.query(Asset.cloud_provider, Asset.id)
            .all()
        )
        provider_counts = Counter(provider for provider, _ in assets_by_provider)

        assets_by_environment = (
            self.db.query(Asset.environment, Asset.id)
            .all()
        )
        environment_counts = Counter(env for env, _ in assets_by_environment)

        apis_by_auth_type = (
            self.db.query(Api.authentication_type, Api.id)
            .all()
        )
        auth_counts = Counter(auth for auth, _ in apis_by_auth_type)

        risk_summary = {
            "high": self.db.query(Asset).filter(Asset.criticality.ilike("%high%")).count(),
            "medium": self.db.query(Asset).filter(Asset.criticality.ilike("%medium%")).count(),
            "low": self.db.query(Asset).filter(Asset.criticality.ilike("%low%")).count(),
        }

        return {
            "total_assets": total_assets,
            "total_apis": total_apis,
            "assets_by_provider": dict(provider_counts),
            "assets_by_environment": dict(environment_counts),
            "apis_by_authentication_type": dict(auth_counts),
            "risk_summary": risk_summary,
        }
