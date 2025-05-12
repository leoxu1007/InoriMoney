from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def new_pay(request):
    return HttpResponse("new pay")


def new_receive(request):
    return HttpResponse("new receive")


def new_transfer(request):
    return HttpResponse("new transfer")


def new_loan(request):
    return HttpResponse("new loan")
