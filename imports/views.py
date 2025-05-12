import os
import shutil
from django.shortcuts import render, HttpResponse
from dbs import dbs
from .forms import UploadStdBillTemplateFileForm
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.utils.datetime_safe import datetime


def upload(request):
    if request.method == "POST":
        form = UploadStdBillTemplateFileForm(request.POST, request.FILES)
        if form.is_valid():
            if handle_uploaded_file(request.FILES["file"]):
                return HttpResponse("Bills imported into db successfully. <a href='/convert'>Go to convert page</a>")
            else:
                return HttpResponse("Bills import failed. <a href='/upload'>Go to import page</a>")
    else:
        form = UploadStdBillTemplateFileForm()
    return render(request, "upload.html", {"form": form})


# TODO tobe modified. because the uploaded file is not specified as std formatted file.
def handle_uploaded_file(in_memory_uploaded_file):
    try:
        uploaded_file_name = "uploaded_file_" + str(int(datetime.now().timestamp())) + ".xlsx"
        FileSystemStorage(location=f"files/uploads/").save(uploaded_file_name, in_memory_uploaded_file)
        import_formatted_xlsx_into_db(f"files/uploads/" + uploaded_file_name)
        return True
    except:
        return False


def import_formatted_xlsx_into_db(formatted_xlsx_file):
    df = pd.read_excel(formatted_xlsx_file)
    list_from_df = df.values.tolist()
    for data_line in list_from_df:
        # if float('-inf') < data_line[1] < float('inf'): continue
        dbs.insert_tb_pay_line(db_file="dbs/book1.db", data=data_line[:8], table="tb_pay")


def clear_cache(request):
    shutil.rmtree(r'files/downloads/')
    os.mkdir(r'files/downloads/')

    shutil.rmtree(r'files/uploads/')
    os.mkdir(r'files/uploads/')

    return HttpResponse("Cache cleared. <a href='/upload'>Go to upload</a>")
