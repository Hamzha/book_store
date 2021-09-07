from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from book_store.admin_dashboard.models import Book, BookMark


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
def product_detail(request):
    book = Book.objects.filter(book_id=16).first()
    bookMarks = BookMark.objects.all()
    return render(request, 'user_dashboard/product_details.html',
                  {'book': book, 'book_id': book.book_id, 'bookMarks': bookMarks})


# def dashboard(request):
#     book = Book.objects.all()
#     return render(request, 'user_dashboard/dashboard.html', {'books': book})


def booK_reader(request, book_id, page_number):
    book = Book.objects.filter(book_id=book_id).values().first()
    return render(request, 'user_dashboard/book_read.html', {'book': book, 'page_number': page_number})


def get_book(request, book_id):
    book = Book.objects.filter(book_id=book_id).values().first()
    return HttpResponse('/media/' + book['pdf'])


def save_bookmark(request, book_id, page_num):
    print(book_id, page_num)
    BookMark.objects.create(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    ).save()
    return HttpResponse('Success')
