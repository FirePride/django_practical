from django.urls import path

from requestdataapp.views import handle_file_upload

app_name = "requestdataapp"

urlpatterns = [
    path("upload/", handle_file_upload, name='file-upload'),
]
