# uploader/urls.py
from django.urls import path
from .views import FileUploadView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('file/<int:id>/', FileUploadView.as_view(), name='file-detail'),  # GET by id
    path('updatefile/<int:id>/', FileUploadView.as_view(), name='file-update'),
    path('deletefile/<int:id>/', FileUploadView.as_view(), name='file-delete'),
    path('files/', FileUploadView.as_view(), name='file-list'), # GET for all files
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
