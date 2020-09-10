from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api.api.endpoints import EditorViewSet, EditorWithJournalsViewSet, JournalViewSet, CustomerViewSet


api_router = DefaultRouter()
api_router.register(r'editors', EditorWithJournalsViewSet)
api_router.register(r'journals', JournalViewSet)
api_router.register(r'customers', CustomerViewSet)


urlpatterns = [
    url(r'^', include(api_router.urls))
]
