from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path


router = DefaultRouter()
router.register(r'data_pipeline', views.ChatbotViewSet, basename='data_pipeline')

urlpatterns = router.urls


urlpatterns = [
    path('load/', views.upload_file, name='upload_pdf'),  
    path('extract/', views.upload_admindata, name='upload_admin'),  
    path('ETL/', views.upload_admindata, name='upload_admin'),  
] + router.urls