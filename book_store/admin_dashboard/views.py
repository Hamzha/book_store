from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from book_store.admin_dashboard.forms import add_book_form, RegisterForm
from book_store.admin_dashboard.models import Book
from book_store.user.models import User


@staff_member_required(login_url='/')
def index(request):
    books = Book.objects.all()
    users = User.objects.all()

    data = {
        'books': books,
        'users': users
    }
    return render(request, 'dashboard/dashboard.html', data)


@staff_member_required(login_url='/')
def add_book(request):
    if request.method == 'POST':
        form = add_book_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('validate')
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = add_book_form()

    return render(request, 'dashboard/add_book.html', {'form': form})


@staff_member_required(login_url='/')
def edit_book(request, book_id):
    if request.method == 'POST':
        obj = get_object_or_404(Book, book_id=book_id)
        form = add_book_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            print('validate')
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = add_book_form(instance=Book.objects.filter(book_id=book_id).first())

    return render(request, 'dashboard/edit_book.html', {'form': form, 'book_id': book_id})


def list_book(request):
    books = Book.objects.all()
    data = {
        'books': books
    }
    return render(request, 'dashboard/book_list.html', data)


def delete_book(request, book_id):
    Book.objects.filter(book_id=book_id).delete()
    print(book_id)
    return HttpResponse({'Success': 'True'})


def add_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            print('valid')
            user.password = make_password(user.password)
            user.save()
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    return render(request, 'dashboard/add_user.html', {'form': RegisterForm()})


def list_user(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})


def edit_user(request, user_id):
    if request.method == 'POST':
        obj = get_object_or_404(User, id=user_id)
        form = RegisterForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = RegisterForm(instance=User.objects.filter(id=user_id).first())

    return render(request, 'dashboard/edit_user.html', {'form': form, 'user_id': user_id})


def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return HttpResponse({'Success': 'True'})

