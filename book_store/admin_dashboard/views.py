from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
from book_store.admin_dashboard.forms import add_book_form


@staff_member_required(login_url='/')
def index(request):
    return render(request, 'dashboard/dashboard.html', {})


@staff_member_required(login_url='/')
def add_book(request):
    if request.method == 'POST':
        form = add_book_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('validate')
    else:
        form = add_book_form()

    return render(request, 'dashboard/add_book.html', {'form': form})
