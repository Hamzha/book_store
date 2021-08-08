from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
@staff_member_required(login_url='/')
def index(request):
    return render(request,'dashboard/dashboard.html',{})
