from django.shortcuts import render, HttpResponse
from django.utils.datetime_safe import datetime
from django.http import FileResponse
from shutil import copyfile
from imports.views import import_formatted_xlsx_into_db
from imports.forms import SelectConvertBillForm
from converts.smart import smart_decide_pay_category_and_program
import csv
import openpyxl

STANDARD_IMPORT_BOOK = "files/blank_template.xlsx"


def index(request):
    if request.method == "POST":
        form = SelectConvertBillForm(request.POST, request.FILES)
        if form.is_valid():
            bill_file = request.FILES["bill_file"]
            bill_type = request.POST["bill_type"]
            # Save the uploaded file to a specific location
            saved_uploaded_bill_file = f"files/uploads/{str(int(datetime.now().timestamp()))}_{bill_file.name}"
            with open(saved_uploaded_bill_file, "wb") as file:
                for chunk in bill_file.chunks():
                    file.write(chunk)
            match bill_type:
                case "1":  # jcb
                    converted_xlsx_file = convert_jcb(jcb_file=saved_uploaded_bill_file)
                case "2":  # 楽天ANA
                    converted_xlsx_file = convert_rakuten(rakuten_file=saved_uploaded_bill_file)
                case _:
                    return HttpResponse("Invalid bill type.")
            try:
                response = FileResponse(open(converted_xlsx_file, "rb"))
                response['Content-Type'] = 'application/octet-stream'
                download_file_name = "InoriMoney_" + converted_xlsx_file[converted_xlsx_file.index("converted_"):]
                response["Content-Disposition"] = f"attachment; filename={download_file_name}"
                return response
            except:
                return HttpResponse("Unable to download the converted file.")
    else:
        form = SelectConvertBillForm()
    return render(request, "select.html", {"form": form})


# write formatted row to converted xlsx
def write_formatted_row_to_converted_xlsx(target_xlsx_file, new_row):
    wb = openpyxl.load_workbook(target_xlsx_file)
    ws = wb["Sheet1"]
    ws._current_row = ws.max_row
    ws.append(new_row)
    wb.save(target_xlsx_file)


# convert jcb csv row line to specified template
def format_jcb_row(row):
    account_id = "acct211"  # acct211 means jcb card
    amount = row[4].replace(",", "")  # paid amount
    category_id, program_id = smart_decide_pay_category_and_program(row[3])
    paid_time = row[2].replace(" ","")
    paid_time = paid_time.replace("/", "-")
    real_time = paid_time
    editor = "converter-jcb"
    memo = " ".join([row[3], row[10], row[9]])
    return [account_id, amount, category_id, paid_time, real_time, program_id, editor, memo]


# convert jcb w card csv file to standard
def convert_jcb(jcb_file):
    target_xlsx_file = "files/downloads/converted_" + str(int(datetime.now().timestamp())) + ".xlsx"
    copyfile(STANDARD_IMPORT_BOOK, target_xlsx_file)
    with open(jcb_file, mode="r", encoding="shift-jis") as csv_f:
        reader = csv.reader(csv_f)
        line_num = 0
        for row in reader:
            if line_num > 5:
                new_row = format_jcb_row(row)
                write_formatted_row_to_converted_xlsx(target_xlsx_file, new_row)
            line_num += 1
    return target_xlsx_file


# convert rakuten ana csv row line to specified template
def format_rakuten_ana_row(row):
    account_id = "acct212"  # acct212 means rakuten ana card
    amount = row[6]  # 支払い総額
    category_id, program_id = smart_decide_pay_category_and_program(row[1])
    paid_time = row[0]
    paid_time = paid_time.replace("/", "-")
    real_time = paid_time
    editor = "converter-ana"
    memo = row[1]
    return [account_id, amount, category_id, paid_time, real_time, program_id, editor, memo]


def convert_rakuten(rakuten_file):
    target_xlsx_file = "files/downloads/converted_" + str(int(datetime.now().timestamp())) + ".xlsx"
    copyfile(STANDARD_IMPORT_BOOK, target_xlsx_file)
    with open(rakuten_file, mode="r", encoding="utf-8") as csv_f:
        reader = csv.reader(csv_f)
        line_num = 0
        for row in reader:
            if line_num > 0:
                if "利用国" in row[1]:
                    row[1] += (" " + reader.__next__()[1])
                row[1] = row[1].replace("\u3000", " ")
                new_row = format_rakuten_ana_row(row)
                write_formatted_row_to_converted_xlsx(target_xlsx_file, new_row)
            line_num += 1
    return target_xlsx_file
