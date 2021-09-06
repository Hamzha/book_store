from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from book_store.admin_dashboard.models import Book


@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login_user(request, user)
            if user.is_admin:
                return redirect('admin-home')
            else:
                return redirect('user-dashboard')

        else:
            return render(request, 'user_dashboard/login.html', {'error': "Please enter correct credentials"})
    return render(request, 'user_dashboard/login.html', {})


# @login_required(login_url='/')
# def dashboard(request):
#     books = Book.objects.filter(book_id=16).first()
#     return render(request, 'user_dashboard/dashboard.html', {'books': books})

@login_required(login_url='/')
def dashboard(request):
    book = Book.objects.filter(book_id=16).values().first()
    return render(request, 'user_dashboard/dashboard.html', {'books': book})


def get_book(request, book_id):
    book = Book.objects.filter(book_id=16).values().first()
    # print('media/'.book.pdf)
    return HttpResponse('media/'+book['pdf'])
    # return FileResponse(open(book.pdf, 'r'), content_type='application/pdf')