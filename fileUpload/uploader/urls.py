# uploader/urls.py
from django.urls import path
from .views import FileUploadView,getFile,getAllFile,deleteFile

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('getfile/<int:id>/',getFile,name = "get-file "),
    path('getallfile/',getAllFile,name = "get-all-file "),
    path('update/<int:id>/',FileUploadView.as_view(),name = "update-file "),
    path('deletefile/<int:id>/',deleteFile,name= "delete-file"),

]
