from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    max_file_size = 2 * (1024 ** 2)  # covert MB to bytes
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES['myfile']
        if myfile.size <= max_file_size:
            fs = FileSystemStorage()
            fs.save(myfile.name, myfile)

        else:
            return render(request, 'requestdataapp/file-size-error.html')

    return render(request, 'requestdataapp/file-upload.html')
