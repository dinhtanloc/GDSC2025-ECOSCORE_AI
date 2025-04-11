from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include


router = DefaultRouter()
router.register(r'', views.ETLViewSet, basename='data_pipeline')

urlpatterns = router.urls


urlpatterns = [
    path('etl/', include(router.urls)),
]