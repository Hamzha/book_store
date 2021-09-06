from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout

# Create your views here.
from book_store.admin_dashboard.forms import book_form, register_form, user_mode_form, deal_voucher_form, \
    user_deal_voucher_form
from book_store.admin_dashboard.models import Book, DealVoucher, DealVoucherUser
from book_store.user.models import User, Mode


@login_required(login_url='/')
def index(request):
    books = Book.objects.all()
    users = User.objects.all()

    data = {
        'books': books,
        'users': users,
    }
    return render(request, 'dashboard/dashboard.html', data)


@login_required(login_url='/')
def add_book(request):
    if request.method == 'POST':
        form = book_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    print('{}: {}'.format(field, item))
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = book_form()
    print('test')
    return render(request, 'dashboard/add_book.html', {'form': form})


@staff_member_required(login_url='/')
def edit_book(request, book_id):
    if request.method == 'POST':
        obj = get_object_or_404(Book, book_id=book_id)
        form = book_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            print('validate')
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = book_form(instance=Book.objects.filter(book_id=book_id).first())

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
    form = register_form()
    if request.method == 'POST':
        form = register_form(request.POST)

        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            print('valid')
            user.password = make_password(user.password)
            user.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    return render(request, 'dashboard/add_user.html', {'form': register_form()})


def list_user(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})


def edit_user(request, user_id):
    if request.method == 'POST':
        obj = get_object_or_404(User, id=user_id)
        form = register_form(request.POST, request.FILES, instance=obj)
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
        form = register_form(instance=User.objects.filter(id=user_id).first())

    return render(request, 'dashboard/edit_user.html', {'form': form, 'user_id': user_id})


def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return HttpResponse({'Success': 'True'})


def add_mode(request):
    form = user_mode_form()
    if request.method == 'POST':
        form = user_mode_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    return render(request, 'dashboard/add_user_mode.html', {'form': form})


def list_user_mode(request):
    modes = Mode.objects.all()
    return render(request, 'dashboard/mode_list.html', {'modes': modes})


def delete_mode(request, mode_id):
    Mode.objects.filter(mode_id=mode_id).delete()
    return HttpResponse({'Success': 'True'})


def edit_user_mode(request, mode_id):
    if request.method == 'POST':
        obj = get_object_or_404(Mode, mode_id=mode_id)
        form = user_mode_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = user_mode_form(instance=Mode.objects.filter(mode_id=mode_id).first())

    return render(request, 'dashboard/edit_user_mode.html', {'form': form, 'mode_id': mode_id})


def add_deal_voucher(request):
    form = deal_voucher_form()
    if request.method == 'POST':
        form = deal_voucher_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    return render(request, 'dashboard/add_deal_voucher.html', {'form': form})


def list_deal_voucher(request):
    vouchers = DealVoucher.objects.all()
    return render(request, 'dashboard/deal_voucher_list.html', {'vouchers': vouchers})


def edit_deal_voucher(request, deal_voucher_id):
    if request.method == 'POST':
        obj = get_object_or_404(DealVoucher, deal_voucher_id=deal_voucher_id)
        form = deal_voucher_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = deal_voucher_form(instance=DealVoucher.objects.filter(deal_voucher_id=deal_voucher_id).first())

    return render(request, 'dashboard/edit_deal_voucher.html', {'form': form, 'deal_voucher_id': deal_voucher_id})


def delete_deal_voucher(request, deal_voucher_id):
    DealVoucher.objects.filter(deal_voucher_id=deal_voucher_id).delete()
    return HttpResponse({'Success': 'True'})


def add_user_deal_voucher(request):
    form = user_deal_voucher_form()
    if request.method == 'POST':
        form = user_deal_voucher_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    return render(request, 'dashboard/add_user_deal_voucher.html', {'form': form})


def list_user_deal_voucher(request):
    vouchers = DealVoucherUser.objects.all()
    return render(request, 'dashboard/user_deal_voucher_list.html', {'vouchers': vouchers})


def delete_user_deal_voucher(request, deal_voucher_user_id):
    DealVoucherUser.objects.filter(deal_voucher_user_id=deal_voucher_user_id).delete()
    return HttpResponse({'Success': 'True'})


def admin_edit_user_deal_voucher(request, deal_voucher_user_id):
    if request.method == 'POST':
        obj = get_object_or_404(DealVoucherUser, deal_voucher_user_id=deal_voucher_user_id)
        form = user_deal_voucher_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = user_deal_voucher_form(
            instance=DealVoucherUser.objects.filter(deal_voucher_user_id=deal_voucher_user_id).first())

    return render(request, 'dashboard/edit_user_deal_voucher.html',
                  {'form': form, 'deal_voucher_user_id': deal_voucher_user_id})


def logout_view(request):
    logout(request)
    return redirect('/')
