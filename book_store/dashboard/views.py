import json
from datetime import datetime
from itertools import chain

from django.contrib import messages
from time import gmtime, strftime

from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.forms.models import model_to_dict

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from book_store.admin_dashboard.models import Book, BookMark, QuickNote, Wishlist, Cart
from book_store.user.forms import RegisterForm


@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('admin-home')
        else:
            # return redirect('/product_detail/17')
            return redirect('user-dashboard')
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
                # return redirect('/product_detail/17')

        else:
            return render(request, 'user_dashboard/login.html', {'error': "Please enter correct credentials"})
    return render(request, 'user_dashboard/login.html', {})


# @login_required(login_url='/')
# def dashboard(request):
#     books = Book.objects.filter(book_id=16).first()
#     return render(request, 'user_dashboard/dashboard.html', {'books': books})


@login_required(login_url='/')
def product_detail(request, product_id):
    book = Book.objects.filter(book_id=product_id).first()
    carts  = Cart.objects.filter(cart_user = request.user)

    book = to_dict(book)
    for cart in carts:
        for book_tmp in cart.cart_book.all():
            if book['book_id'] == book_tmp.book_id:
                book['is_buy'] = True
    return render(request, 'user_dashboard/product_details.html',
                  {'book': book, 'book_id': book['book_id']})


# def dashboard(request):
#     book = Book.objects.all()
#     return render(request, 'user_dashboard/dashboard.html', {'books': book})


def booK_reader(request, book_id, page_number=1):
    book = Book.objects.filter(book_id=book_id).first()

    bookmarks = BookMark.objects.filter(bookmark_book=book, bookmark_user=request.user)

    if book.book_type != 'AUDIO':
        return render(request, 'user_dashboard/book_read.html',
                      {'book': book, 'page_number': page_number, 'bookMarks': bookmarks})
    else:
        bookmark_list = []
        for bookmark in bookmarks:
            tmp = to_dict(bookmark)
            tmp['bookmark_page_number_sec'] = strftime("%H:%M:%S", gmtime(tmp['bookmark_page_number']))
            bookmark_list.append(tmp)
            print(tmp)

    return render(request, 'user_dashboard/book_listen.html',
                  {'book': book, 'bookMarks': bookmark_list})


def get_book(request, book_id):
    book = Book.objects.filter(book_id=book_id).values().first()
    print(book['book_type'])
    if book['book_type'] == 'PDF':
        return HttpResponse('/media/' + book['pdf'])
    else:
        return HttpResponse('/media/' + book['audio'])


def save_bookmark(request, book_id, page_num):
    BookMark.objects.create(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    ).save()
    return HttpResponse('Success')


def remove_bookmark(request, book_id, page_num):
    BookMark.objects.filter(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    ).delete()

    return HttpResponse('Success')


def get_bookmark(request,book_id):
    bookMarks = BookMark.objects.filter(bookmark_book = book_id)
    bookMarks = serializers.serialize('json', bookMarks)
    return HttpResponse(bookMarks, content_type="text/json-comment-filtered")


def get_quick_notes(request):
    quick_notes = QuickNote.objects.all()
    quick_notes = serializers.serialize('json', quick_notes)
    return HttpResponse(quick_notes, content_type="text/json-comment-filtered")


def save_quick_notes(request, book_id, page_num):
    QuickNote.objects.create(
        QuickNote_book=Book.objects.filter(book_id=book_id).first(),
        QuickNote_user=request.user,
        QuickNote_page_number=page_num,
        QuickNote_text=request.GET['data']
    ).save()
    return HttpResponse('success')


def signup(request):
    print('called')
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return render(request, 'user_dashboard/login.html', {})

        else:
            print('form.errors', form.errors)
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

            return render(request, 'user_dashboard/sign_up.html', {'form': RegisterForm})

    else:
        return render(request, 'user_dashboard/sign_up.html', {'form': RegisterForm})


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def dashboard(request):
    books = Book.objects.all()
    wishlists = Wishlist.objects.filter(wishlist_user=request.user)
    carts = Cart.objects.filter(cart_user = request.user)

    book_list = []
    wishlist_list = []

    for book in books:
        book_list.append(to_dict(book))
    for wishlist in wishlists:
        wishlist_list.append(to_dict(wishlist))

    for book_index, book_item in enumerate(book_list):
        for wishlist_index, wishlist_item in enumerate(wishlist_list):
            if book_item['book_id'] == wishlist_item['wishlist_book']:
                book_list[book_index]['book_wishlist'] = wishlist_item
        for cart in carts:
            for book in cart.cart_book.all():
                if book_item['book_id'] == book.book_id:
                    book_list[book_index]['is_buy'] = True

    # for book in books:
    #     for wishlist in wishlists:
    #         if book.book_id == wishlist.wishlist_book.book_id:
    #             book.wishlist = True
    # print(books.wishlist)
    return render(request, 'user_dashboard/home.html', {'books': book_list, 'wishlists': wishlists})


def set_wishlist(request, book_id):
    Wishlist.objects.create(
        wishlist_user=request.user,
        wishlist_book=Book.objects.filter(book_id=book_id).first()
    ).save()
    print('test')
    return HttpResponse('Success')


def remove_wishlist(request, book_id):
    Wishlist.objects.filter(wishlist_book=Book.objects.filter(book_id=book_id).first()).delete()
    return HttpResponse('Success')


def add_to_cart(request, book_id):
    if request.method == 'GET':
        print('test')
        print(request.GET('data'))
    cart = Cart.objects.create(
        cart_user=request.user
    )
    data = serializers.serialize('json', [cart], ensure_ascii=False)
    return JsonResponse(data, content_type="application/json", safe=False)


def set_cart(request):
    if request.method == 'GET':
        tmp = request.GET.dict()['cart']
        request.session['book_list'] = tmp

    return HttpResponse('Success')


def cart(request):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    print(type(book_list_ids), book_list_ids)
    books = Book.objects.filter(pk__in=book_list_ids)
    total = 0
    for book in books:
        total = book.price + total
    return render(request, 'user_dashboard/cart.html', {'books': books, 'total': total})


def cart_payment(request):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    print(type(book_list_ids), book_list_ids)
    books = Book.objects.filter(pk__in=book_list_ids)
    cart = Cart.objects.create(cart_user=request.user, payment_status='Paid', cart_detail='Paid')
    for book in books:
        cart.cart_book.add(book)
    cart.save()
    return HttpResponse('Success')


def user_portal(request):
    wishlist = Wishlist.objects.filter(wishlist_user=request.user)
    print(wishlist)
    carts = Cart.objects.filter(cart_user = request.user)
    
    print(carts)
    return render(request, 'user_dashboard/user_portal.html', {'wishlists': wishlist, 'user': request.user, 'carts': carts})
