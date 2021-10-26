import json
import random
import string
from datetime import datetime
from itertools import chain
import uuid;
from django.contrib import messages
from time import gmtime, strftime

from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.forms.models import model_to_dict

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from book_store.admin_dashboard.models import Book, BookMark, QuickNote, Wishlist, Cart, Review, Deal, VoucherUser, \
    Voucher, Quiz
from book_store.user.forms import RegisterForm
from book_store.user.models import User

discount_voucher = 0


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


@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def product_detail(request, product_id):
    book = Book.objects.filter(book_id=product_id).first()
    carts = Cart.objects.filter(cart_user=request.user)
    wishlists = Wishlist.objects.filter(wishlist_user=request.user)

    book = to_dict(book)
    wishlist_list = []
    for wishlist in wishlists:
        wishlist_list.append(to_dict(wishlist))

    for cart in carts:
        for book_tmp in cart.cart_book.all():
            if book['book_id'] == book_tmp.book_id:
                book['is_buy'] = True

    summary = book['summary'][:int(len(book['summary']) / 2)], book['summary'][int(len(book['summary']) / 2):]

    reviews = Review.objects.filter(review_book=book['book_id'])
    print(reviews)
    rating = 0
    for review in reviews:
        rating = rating + review.review_rate
    try:
        rating = int(rating / len(reviews))
    except:
        rating = 0
    return render(request, 'user_dashboard/product_details_2.html',
                  {'book': book, 'book_id': book['book_id'], 'summary': summary, 'year': book['year_of_publish'].year,
                   'month': book['year_of_publish'].strftime("%b"), 'day': book['year_of_publish'].day,
                   'reviews': reviews, 'ratings': rating})


# def dashboard(request):
#     book = Book.objects.all()
#     return render(request, 'user_dashboard/dashboard.html', {'books': book})

@login_required(login_url='/')
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


@login_required(login_url='/')
def get_book(request, book_id):
    book = Book.objects.filter(book_id=book_id).values().first()
    print(book['book_type'])
    if book['book_type'] == 'PDF':
        return HttpResponse('/media/' + book['pdf'])
    else:
        return HttpResponse('/media/' + book['audio'])


@login_required(login_url='/')
def save_bookmark(request, book_id, page_num):
    BookMark.objects.create(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    ).save()
    return HttpResponse('Success')


@login_required(login_url='/')
def remove_bookmark(request, book_id, page_num):
    BookMark.objects.filter(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    ).delete()

    return HttpResponse('Success')


@login_required(login_url='/')
def get_bookmark(request, book_id):
    bookMarks = BookMark.objects.filter(bookmark_book=book_id)
    bookMarks = serializers.serialize('json', bookMarks)
    return HttpResponse(bookMarks, content_type="text/json-comment-filtered")


@login_required(login_url='/')
def get_quick_notes(request, book_id):
    quick_notes = QuickNote.objects.all()
    quick_notes = serializers.serialize('json', quick_notes)
    return HttpResponse(quick_notes, content_type="text/json-comment-filtered")


@login_required(login_url='/')
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
    print(Voucher.objects.filter(voucher_id=1).first())
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            voucherUser = VoucherUser.objects.create(user=user, voucher=Voucher.objects.filter(voucher_id=1).first())
            voucherUser.save()
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


@login_required(login_url='/')
def dashboard(request):
    books = Book.objects.all()
    wishlists = Wishlist.objects.filter(wishlist_user=request.user)
    carts = Cart.objects.filter(cart_user=request.user)

    book_list = []
    wishlist_list = []

    for book in books:
        book.year_of_publish = book.year_of_publish.year
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
        book_list[book_index]['summary'] = book_list[book_index]['summary'][:126] + '...'

    child = [book for book in book_list if book['adult_mode'] == False]
    adult = [book for book in book_list if book['adult_mode'] == True]

    best_seller = [book for book in child if book['best_seller'] == True]
    books = [book for book in child if book['best_seller'] == False]

    data = datetime.now().replace(tzinfo=None) - request.user.date_of_birth.replace(tzinfo=None)

    return render(request, 'user_dashboard/home.html', {'books': books,
                                                        'best_seller': best_seller,
                                                        'adults': adult,
                                                        'age': data.days / 360,
                                                        'wishlists': wishlists})


@login_required(login_url='/')
def set_wishlist(request, book_id):
    Wishlist.objects.create(
        wishlist_user=request.user,
        wishlist_book=Book.objects.filter(book_id=book_id).first()
    ).save()
    print('test')
    return HttpResponse('Success')


@login_required(login_url='/')
def remove_wishlist(request, book_id):
    Wishlist.objects.filter(wishlist_book=Book.objects.filter(book_id=book_id).first()).delete()
    return HttpResponse('Success')


@login_required(login_url='/')
def add_to_cart(request, book_id):
    if request.method == 'GET':
        print('test')
        print(request.GET('data'))
    cart = Cart.objects.create(
        cart_user=request.user
    )
    data = serializers.serialize('json', [cart], ensure_ascii=False)
    return JsonResponse(data, content_type="application/json", safe=False)


@login_required(login_url='/')
def set_cart(request):
    if request.method == 'GET':
        tmp = request.GET.dict()['cart']
        request.session['book_list'] = tmp

    return HttpResponse('Success')


@login_required(login_url='/')
def cart(request):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    books = Book.objects.filter(pk__in=book_list_ids)

    deals = Deal.objects.all()
    deals = [deal for deal in deals if deal.deal_valid_upto > datetime.now().date()]

    for deal in deals:
        for deal_book in deal.deal_book.all():
            for book in books:
                if book.book_id == deal_book.book_id:
                    book.percentage = deal.deal_percentage
    total = 0
    for book in books:
        try:
            total = (float(book.price) - (float(book.price) * (book.percentage / 100))) + total
            print(total)
        except Exception as ex:
            total = float(book.price) + total
    print(total)
    return render(request, 'user_dashboard/cart.html', {'books': books, 'total': total})


@login_required(login_url='/')
def cart_payment(request):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    books = Book.objects.filter(pk__in=book_list_ids)
    cart = Cart.objects.create(cart_user=request.user, payment_status='Paid', cart_detail='Paid')
    for book in books:
        cart.cart_book.add(book)
    cart.save()
    return HttpResponse('Success')


@login_required(login_url='/')
def user_profile(request):
    wishlist = Wishlist.objects.filter(wishlist_user=request.user)
    carts = Cart.objects.filter(cart_user=request.user)
    user_Vouchers = VoucherUser.objects.filter(user=request.user)
    return render(request, 'user_dashboard/user_profile.html',
                  {'wishlists': wishlist, 'user': request.user, 'carts': carts, 'user_vouchers': user_Vouchers})


@login_required(login_url='/')
def checkout(request):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    books = Book.objects.filter(pk__in=book_list_ids)
    deals = Deal.objects.all()
    deals = [deal for deal in deals if deal.deal_valid_upto > datetime.now().date()]

    for deal in deals:
        for deal_book in deal.deal_book.all():
            for book in books:
                if book.book_id == deal_book.book_id:
                    book.percentage = deal.deal_percentage

    total = 0
    book_total = 0
    for book in books:
        book_total = book_total + book.price
        try:
            total = (float(book.price) - (float(book.price) * (book.percentage / 100))) + total
        except Exception as ex:
            total = float(book.price) + total
    discount = book_total - total
    print(total)
    global discount_voucher
    total = total - discount_voucher
    print(total)
    return render(request, 'user_dashboard/checkout.html',
                  {'books': books, 'amount': total, 'book_total': book_total, 'discount': discount})


@login_required(login_url='/')
def user_profile_update(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        print(data)
        if not request.user.check_password(data['current_password']):

            return HttpResponse(JsonResponse({"error": "Current password is not correct"}))
        else:
            print(data)
            User.objects \
                .filter(username=request.user.username) \
                .update(first_name=data['first_name'], last_name=data['last_name'], username=data['username'],
                        email=data['email']
                        )

            user = User.objects.get(username=request.user.username)
            user.set_password(data['new_password'])
            user.save()
    return HttpResponse(JsonResponse({'response': 'test'}))


@login_required(login_url='/')
def review_book(request, book_id):
    book = Book.objects.filter(book_id=book_id).first()
    return render(request, 'user_dashboard/review.html', {'book': book})


@login_required(login_url='/')
def wishlist(request):
    wishlist = Wishlist.objects.filter(wishlist_user=request.user)
    return render(request, 'user_dashboard/wishlist.html', {'wishlists': wishlist})


@login_required(login_url='/')
def review_save_book(request, book_id):
    print(book_id)
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        Review.objects.create(
            review_user=request.user,
            review_book=Book.objects.filter(book_id=book_id).first(),
            review_text=data['review'],
            review_rate=data['rating']
        ).save()

    return HttpResponse('Success')


@login_required(login_url='/')
def deal_discounts(request):
    deals = Deal.objects.all()
    deals = [deal for deal in deals if deal.deal_valid_upto > datetime.now().date()]

    return render(request, 'user_dashboard/deal.html', {'deals': deals})


def voucher_list(request):
    vouchers = VoucherUser.objects.filter(user=request.user)
    print(vouchers)
    return render(request, 'user_dashboard/voucher_list.html', {'vouchers': vouchers})


def voucher_check(request):
    if request.method == 'GET':
        final = None
        data = json.loads(request.GET.dict()['data'])
        vouchers = VoucherUser.objects.filter(user=request.user)
        final_voucher = None
        for voucher in vouchers:
            if voucher.voucher.code == data['code']:
                final = voucher.voucher
                final_voucher = voucher
        json_data = json.dumps({'voucher': 'None'})
        if final is not None:
            json_data = json.dumps({'voucher': to_dict(final)})
            global discount_voucher
            discount_voucher = final.credit
            final_voucher.delete()

    return HttpResponse(json_data, content_type="application/json")


def attempt_quiz(request, book_id):
    book = Book.objects.filter(book_id=book_id).first()
    quiz = Quiz.objects.filter(quiz_book=book)
    print(quiz)
    return render(request, 'user_dashboard/attempt_quiz.html', {'book': book, 'quizs': quiz})


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def check_answer(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        score = 0
        for elmt in data['obj']:
            quiz_id = elmt['quiz_id']
            answer = elmt['answer']
            print(elmt)
            print('quiz_id',quiz_id)
            quiz = Quiz.objects.filter(quiz_id=quiz_id).first()
            if quiz.quiz_answer == answer:
                code = uuid.uuid4().hex.upper()[0:6]
                Voucher.objects.create(description='For pass the Question',
                                       credit=20, code=code).save()
                voucher = Voucher.objects.filter(
                    voucher_id=Voucher.objects.filter(code=code).first().voucher_id
                ).first()

                VoucherUser.objects.create(voucher=voucher, user=request.user).save()
                score = score +1

    json_data = json.dumps({'result': score})

    # return HttpResponse('Success')
    return HttpResponse(json_data, content_type="application/json")
