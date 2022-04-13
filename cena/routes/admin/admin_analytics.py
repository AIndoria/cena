from functools import cached_property

from fastapi import APIRouter

from cena.routes._base import BaseAdminController, controller
from cena.schema.analytics.analytics import CenaAnalytics
from cena.services.analytics.service_analytics import AnalyticsService

router = APIRouter(prefix="/analytics")


@controller(router)
class AdminAboutController(BaseAdminController):
    @cached_property
    def service(self) -> AnalyticsService:
        return AnalyticsService(self.repos)

    @router.get("", response_model=CenaAnalytics)
    def get_analytics(self):
        return self.service.calculate_analytics()
