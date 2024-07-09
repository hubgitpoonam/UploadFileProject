# uploader/urls.py
from django.urls import path
from .views import FileUploadView,getFile,getAllFile,UpdateFile,deleteFile

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('getfile/<int:id>/',getFile,name = "get-file "),
    path('getallfile/',getAllFile,name = "get-all-file "),
    path('updatefile/<int:id>/',UpdateFile,name = "update-file "),
    path('deletefile/<int:id>/',deleteFile,name= "delete-file"),

]
