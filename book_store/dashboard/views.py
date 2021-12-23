import json
import random
import string
from datetime import datetime, timezone
from itertools import chain
import uuid;
from django.contrib import messages
from time import gmtime, strftime

from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.core import serializers
from django.forms.models import model_to_dict

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from mailjet_rest import Client

from book_store.admin_dashboard.models import Book, BookMark, QuickNote, Wishlist, Cart, Review, Deal, VoucherUser, \
    Voucher, Quiz, BookAudio, QueryFeedback
from book_store.dashboard.forms import queryFeedbackForm
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
    rating = 0
    for review in reviews:
        rating = rating + review.review_rate
    try:
        rating = int(rating / len(reviews))
    except:
        rating = 0
    audio = BookAudio.objects.filter(book=book['book_id'])
    recommandation = Book.objects.filter(genre=book['genre'])

    return render(request, 'user_dashboard/product_details_2.html',
                  {'book': book, 'book_id': book['book_id'], 'summary': summary, 'year': book['year_of_publish'].year,
                   'month': book['year_of_publish'].strftime("%b"), 'day': book['year_of_publish'].day,
                   'reviews': reviews, 'ratings': rating, 'audios': audio, 'recommandations': recommandation})


# def dashboard(request):
#     book = Book.objects.all()
#     return render(request, 'user_dashboard/dashboard.html', {'books': book})

@login_required(login_url='/')
def booK_reader(request, book_id, page_number=1):
    book = Book.objects.filter(book_id=book_id).first()

    bookmarks = BookMark.objects.filter(bookmark_book=book, bookmark_user=request.user)
    return render(request, 'user_dashboard/book_read.html',
                  {'book': book, 'page_number': page_number, 'bookMarks': bookmarks})

    # if book.book_type != 'BOTH':
    #     return render(request, 'user_dashboard/book_read.html',
    #                   {'book': book, 'page_number': page_number, 'bookMarks': bookmarks})
    # else:
    #     bookmark_list = []
    #     for bookmark in bookmarks:
    #         tmp = to_dict(bookmark)
    #         tmp['bookmark_page_number_sec'] = strftime("%H:%M:%S", gmtime(tmp['bookmark_page_number']))
    #         bookmark_list.append(tmp)
    #
    # return render(request, 'user_dashboard/book_listen.html',
    #               {'book': book, 'bookMarks': bookmark_list})


@login_required(login_url='/')
def get_book(request, book_id, chapter_id):
    book = Book.objects.filter(book_id=book_id).values().first()
    if book['book_type'] == 'PDF':
        return HttpResponse('/media/' + book['pdf'])
    else:

        type = json.loads(request.GET.dict()['data'])
        if (type['type'] == 'pdf'):
            return HttpResponse('/media/' + book['pdf'])
        else:
            audio = BookAudio.objects.filter(book=Book.objects.filter(book_id=book_id).first(),
                                             audio_id=chapter_id).first()
        return HttpResponse('/media/' + str(audio.audio))


@login_required(login_url='/')
def get_book_pdf(request, book_id, chapter_id):
    print('asdfasdf')
    book = Book.objects.filter(book_id=book_id).values().first()
    return HttpResponse('/media/' + book['pdf'])


@login_required(login_url='/')
def save_bookmark(request, book_id, page_num):
    bookmark = BookMark.objects.create(
        bookmark_book=Book.objects.filter(book_id=book_id).first(),
        bookmark_user=request.user,
        bookmark_page_number=page_num
    )
    try:
        if request.method == 'GET':
            if request.GET['chapter'] != None:
                audio = BookAudio.objects.filter(audio_id=request.GET['chapter']).first()
                bookmark.bookmark_audio = audio
                bookmark.save()
    except:
        pass
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
    quick_notes = QuickNote.objects.filter(QuickNote_book=Book.objects.filter(book_id=book_id).first())
    quick_notes = serializers.serialize('json', quick_notes)
    return HttpResponse(quick_notes, content_type="text/json-comment-filtered")


@login_required(login_url='/')
def save_quick_notes(request, book_id, page_num):
    print(book_id, page_num, 'test')

    if request.method == 'GET':
        data = json.loads(request.GET['data'])
        if data['type'] == 'audio':

            if QuickNote.objects.filter(QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                                        QuickNote_user=request.user,
                                        QuickNote_page_number=page_num,
                                        ).exists():
                QuickNote.objects.filter(QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                                         QuickNote_user=request.user,
                                         QuickNote_page_number=page_num,
                                         ).delete()

            QuickNote.objects.create(
                QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                QuickNote_user=request.user,
                QuickNote_page_number=page_num,
                QuickNote_audio_book=BookAudio.objects.filter(audio_id=page_num).first(),
                QuickNote_text=data['text']
            ).save()
        else:
            if QuickNote.objects.filter(QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                                        QuickNote_user=request.user,
                                        QuickNote_page_number=page_num,
                                        ).exists():
                QuickNote.objects.filter(QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                                         QuickNote_user=request.user,
                                         QuickNote_page_number=page_num,
                                         ).delete()

            QuickNote.objects.create(
                QuickNote_book=Book.objects.filter(book_id=book_id).first(),
                QuickNote_user=request.user,
                QuickNote_page_number=page_num,
                QuickNote_text=data['text']
            ).save()
            print('test')
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
            user = User.objects.filter(id= user.id).first()
            code = uuid.uuid4().hex.upper()[0:6]

            Voucher.objects.create(description='Signup Voucher',
                                   credit=200, code=code).save()
            voucher = Voucher.objects.filter(
                voucher_id=Voucher.objects.filter(code=code).first().voucher_id
            ).first()

            VoucherUser.objects.create(voucher=voucher, user=user).save()
            books = Book.objects.filter(free_book = True)
            cart = Cart.objects.create(cart_user=user, payment_status='Paid', cart_detail='Paid')
            for book in books:
                cart.cart_book.add(book)
            cart.save()

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
    print(request.user.email)
    return render(request, 'user_dashboard/home.html', {'books': books,
                                                        'best_seller': best_seller,
                                                        'adults': adult,
                                                        'age': data.days / 360,
                                                        'wishlists': wishlists,
                                                        'email':request.user.email})


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
    print(book_list_ids)
    if len(book_list_ids) == 2:
        return redirect('user-dashboard')
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]
    books = Book.objects.filter(pk__in=book_list_ids)
    wishlist = []
    deals = Deal.objects.all()
    deals = [deal for deal in deals if deal.deal_valid_upto > datetime.now().date()]

    for deal in deals:
        for deal_book in deal.deal_book.all():
            for book in books:
                if book.book_id == deal_book.book_id:
                    book.percentage = deal.deal_percentage
    total = 0
    for book in books:
        wish = Wishlist.objects.filter(wishlist_user=request.user, wishlist_book=book).first()
        if wish:
            book.wishlist_book = True
        try:
            total = (float(book.price) - (float(book.price) * (book.percentage / 100))) + total
            print(total)
        except Exception as ex:
            total = float(book.price) + total
    print(books)

    recommandation = Book.objects.filter(genre=books[0].genre)
    print(recommandation)
    return render(request, 'user_dashboard/cart.html',
                  {'books': books, 'total': total, 'recommandations': recommandation, 'wishlists': wishlist})


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

    if len(books) >= 5:
        code = uuid.uuid4().hex.upper()[0:6]
        Voucher.objects.create(description='For Buying 5 books',
                               credit=100, code=code).save()
        voucher = Voucher.objects.filter(
            voucher_id=Voucher.objects.filter(code=code).first().voucher_id
        ).first()

        VoucherUser.objects.create(voucher=voucher, user=request.user).save()

    return HttpResponse('Success')


@login_required(login_url='/')
def user_profile(request):
    wishlist = Wishlist.objects.filter(wishlist_user=request.user)
    carts = Cart.objects.filter(cart_user=request.user)
    user_Vouchers = VoucherUser.objects.filter(user=request.user)
    print(carts)
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

    author = Book.objects.values('author').distinct()
    if "filter_book" in request.session.keys():
        print('request.session["filter_book"]', request.session["filter_book"])

        book_list = []
        [book_list.append(book) for book in wishlist if book.wishlist_book.book_id in request.session['filter_book']]

        del request.session["filter_book"]
        return render(request, 'user_dashboard/wishlist.html', {'wishlists': book_list, 'authors': author})

    return render(request, 'user_dashboard/wishlist.html', {'wishlists': wishlist, 'authors': author})


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


@login_required(login_url='/')
def voucher_list(request):
    vouchers = VoucherUser.objects.filter(user=request.user)
    print(vouchers)
    return render(request, 'user_dashboard/voucher_list.html', {'vouchers': vouchers})


@login_required(login_url='/')
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


@login_required(login_url='/')
def attempt_quiz(request, book_id):
    book = Book.objects.filter(book_id=book_id).first()
    quiz = Quiz.objects.filter(quiz_book=book).all().order_by('?')[0:10]

    return render(request, 'user_dashboard/attempt_quiz.html', {'book': book, 'quizs': quiz})


@login_required(login_url='/')
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@login_required(login_url='/')
def check_answer(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        score = 0
        for elmt in data['obj']:
            quiz_id = elmt['quiz_id']
            answer = elmt['answer']
            print(elmt)
            print('quiz_id', quiz_id)
            quiz = Quiz.objects.filter(quiz_id=quiz_id).first()
            if quiz.quiz_answer == answer:
                score = score + 2

        # q1 - 2 * 2.5 = 5
        # q2 - 2 * 2.5 = 5
        # 4 * 2.5 = 10
        if score != 0:
            credit = score * 2.5
            code = uuid.uuid4().hex.upper()[0:6]
            Voucher.objects.create(description='For pass the Question',
                                   credit=credit, code=code).save()
            voucher = Voucher.objects.filter(
                voucher_id=Voucher.objects.filter(code=code).first().voucher_id
            ).first()

            VoucherUser.objects.create(voucher=voucher, user=request.user).save()

    json_data = json.dumps({'result': score})

    # return HttpResponse('Success')
    return HttpResponse(json_data, content_type="application/json")


@login_required(login_url='/')
def booK_listen(request, book_id):
    book = Book.objects.filter(book_id=book_id).first()
    audio = BookAudio.objects.filter(book=book)
    return render(request, 'user_dashboard/book_listen_2.html', {'book': book, 'audio': audio})


@login_required(login_url='/')
def booK_listen_chapter(request, book_id, chapter):
    book = Book.objects.filter(book_id=book_id).first()
    audio = BookAudio.objects.filter(book=book, audio_id=chapter).first()
    bookmark = BookMark.objects.filter(bookmark_book=book, bookmark_user=request.user, bookmark_audio=audio)
    quickNote = QuickNote.objects.filter(QuickNote_book=book, QuickNote_user=request.user, QuickNote_audio_book=audio)
    for index, mark in enumerate(bookmark):
        mark.time = strftime("%H:%M:%S", gmtime(mark.bookmark_page_number))
    return render(request, 'user_dashboard/book_listen_2.html',
                  {'book': book, 'audio': audio, 'bookmarks': bookmark, 'quickNote': quickNote})


def user_author_menu(request):
    books = Book.objects.filter(book_user=request.user)
    print(books)
    return render(request, 'user_dashboard/user_author_menu.html', {'books': books})


@csrf_exempt
def user_author_add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        year_of_publish = request.POST.get('year_of_publish')
        no_of_pages = request.POST.get('no_of_pages')
        genre = request.POST.get('genre')
        price = request.POST.get('price')
        author = request.POST.get('author')
        adult_mode = request.POST.get('adult_mode')
        best_seller = request.POST.get('best_seller')
        free_book = request.POST.get('free_book')
        summary = request.POST.get('summary')
        cover_photo = request.FILES['cover_photo']

        book_type = request.POST.get('book_type')
        pdf = request.FILES['pdf']
        fs = FileSystemStorage()
        pdf = fs.save(pdf.name, pdf)
        cover_photo = fs.save(cover_photo.name, cover_photo)

        year_of_publish = datetime(int(year_of_publish), month=1, day=1).date()
        print(adult_mode)
        if adult_mode is None:
            adult_mode = False
        else:
            adult_mode = True
        if free_book is None:
            free_book = False
        else:
            free_book = True
        if best_seller is None:
            best_seller = False
        else:
            best_seller = True

        audios = []
        if book_type == 'BOTH':
            audios = request.FILES.getlist("file[]")
            book = Book.objects.create(
                title=title,
                year_of_publish=year_of_publish,
                no_of_pages=no_of_pages,
                genre=genre,
                price=price,
                author=author,
                cover_photo=cover_photo,
                book_type=book_type,
                pdf=pdf,
                summary=summary,
                adult_mode=adult_mode,
                free_book=free_book,
                best_seller=best_seller,
                book_user=request.user
            )
            book.save()
            send_mail(book)
            if book.free_book:
                for user in User.objects.all():
                    cart = Cart.objects.create(cart_user=user, payment_status='Paid', cart_detail='Paid')
                    cart.cart_book.add(Book.objects.filter(book_id=book.book_id).first())
            for audio in audios:
                audio_file = fs.save(audio.name, audio)
                BookAudio.objects.create(book=book,
                                         audio=audio_file).save()
        else:
            book = Book.objects.create(
                title=title,
                year_of_publish=year_of_publish,
                no_of_pages=no_of_pages,
                genre=genre,
                price=price,
                author=author,
                cover_photo=cover_photo,
                book_type=book_type,
                pdf=pdf,
                summary=summary,
                adult_mode=adult_mode,
                free_book=free_book,
                best_seller=best_seller,
                book_user=request.user
            )
            book.save()
            send_mail(book)

            if book.free_book:
                for user in User.objects.all():
                    cart = Cart.objects.create(cart_user=user, payment_status='Paid', cart_detail='Paid')
                    cart.cart_book.add(Book.objects.filter(book_id=book.book_id).first())
    return render(request, 'user_dashboard/add_book.html', {})


def user_delete_book(request, book_id):
    Book.objects.filter(book_id=book_id).delete()
    return HttpResponse('Success')


def user_get_genre_book(request, genre):
    books = Book.objects.filter(genre__icontains=genre)
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)
    books_list = []
    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    books_list_final = []
    print(books_list)
    # if diff < 18:
    #     books_list_final = [book for book in books_list if book['adult_mode'] != True]

    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list, 'genre': genre})


def user_get_best_book(request):
    books = Book.objects.filter(best_seller=True)
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)
    books_list = []
    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    books_list_final = []
    print(books_list)
    # if diff < 18:
    #     books_list_final = [book for book in books_list if book['adult_mode'] != True]
    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list})


def user_get_best_book(request):
    books = Book.objects.filter(best_seller=True)
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)

    books_list = []

    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    books_list_final = []
    print(books_list)
    # if diff < 18:
    #     books_list_final = [book for book in books_list if book['adult_mode'] != True]
    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list, 'genre': 'Best Seller'})


def user_get_audio_book(request):
    books = Book.objects.filter(book_type="BOTH")
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)

    books_list = []

    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    books_list_final = []
    print(books_list)
    # if diff < 18:
    #     books_list_final = [book for book in books_list if book['adult_mode'] != True]
    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list, 'genre': 'Audio and PDF'})


def user_get_pdf_book(request):
    books = Book.objects.filter(book_type="PDF")
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)

    books_list = []

    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    books_list_final = []
    print(books_list)
    # if diff < 18:
    #     books_list_final = [book for book in books_list if book['adult_mode'] != True]
    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list, 'genre': 'PDF Books'})


def user_search_book(request, search):
    books = Book.objects.filter(
        Q(title__icontains=search) | Q(genre__icontains=search) | Q(author__icontains=search) | Q(
            summary__icontains=search))
    diff = 12

    diff = datetime.now(timezone.utc) - request.user.date_of_birth
    diff = diff.seconds / (365.25 * 24 * 60 * 60)

    books_list = []

    if diff < 18:
        [books_list.append(to_dict(book)) for book in books if book.adult_mode == False]
    else:
        [books_list.append(to_dict(book)) for book in books]
    for index, book in enumerate(books_list):
        reviews = Review.objects.filter(review_book=book['book_id'])
        rating = 0
        for review in reviews:
            rating = rating + review.review_rate
        try:
            rating = int(rating / len(reviews))
        except:
            rating = 0
        books_list[index]['rating'] = rating
    return render(request, 'user_dashboard/book_by_genre.html', {'books': books_list, 'genre': search})


def send_mail(book):
    api_key = '21b0378ce48d6aa976e690ccaef126cc'
    api_secret = '6e3f27dce05716d6b7e45739dcdd93ac'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "ayesharaig786@gmail.com",
                    "Name": "Ayesha"
                },
                "To": [
                    {
                        "Email": "ahmedhamza884@gmail.com",
                        "Name": "Ayesha"
                    }
                ],
                "Subject": "New Book Added",
                "TextPart": "My first Mailjet email",
                "HTMLPart": "Dear beloved customer! A new Book is added in the Book Store. <br /> Name: " + book.title +
                            "<br />Author: " + book.author + "<br /> Feel Free to visit anytime.<br /> Regards Book Store Co.",

            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return HttpResponse('test')


def user_filter_book(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        print(data)

        print(data['price'])
        books = []
        book_list = Book.objects.all()

        for price in data['price']:
            print(price)
            if price == '0':
                [books.append(book.book_id) for book in book_list if book.free_book == True]
            if price == '1':
                [books.append(book.book_id) for book in book_list if 0 <= book.price <= 500]
            if price == '2':
                [books.append(book.book_id) for book in book_list if 501 <= book.price <= 1000]
            if price == '3':
                [books.append(book.book_id) for book in book_list if 1001 <= book.price <= 1500]
            if price == '4':
                [books.append(book.book_id) for book in book_list if book.price >= 1501]
        print('books', books)
        for author in data['author']:
            [books.append(book.book_id) for book in book_list if book.author == author]

        for rating in data['rating']:
            for book in book_list:
                review = Review.objects.filter(review_book=book).all()
                if review:
                    if rating == '0':
                        [books.append(book.review_book.book_id) for book in review if 4.5 <= book.review_rate <= 5]
                    if rating == '1':
                        [books.append(book.review_book.book_id) for book in review if 4.0 <= book.review_rate <= 4.5]

                    if rating == '2':
                        [books.append(book.review_book.book_id) for book in review if 3.5 <= book.review_rate <= 4.0]

                    if rating == '3':
                        [books.append(book.review_book.book_id) for book in review if 3.0 <= book.review_rate <= 3.5]

                    if rating == '4':
                        [books.append(book.review_book.book_id) for book in review if 2.5 <= book.review_rate <= 3]

                    if rating == '5':
                        [books.append(book.review_book.book_id) for book in review if 0 <= book.review_rate <= 2.5]

    request.session['filter_book'] = books
    print('book_id', books)
    return HttpResponse('success')


def wishlist_sort(request, sort):
    wishlists = Wishlist.objects.filter(wishlist_user=request.user)
    book_list = []
    print(wishlists)
    if sort == '1':
        [book_list.append(wishlist) for wishlist in wishlists if wishlist.wishlist_book.best_seller == True]
    if sort == '2':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by("wishlist_book__title")
    if sort == '3':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by("wishlist_book__title").reverse()
    if sort == '4':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by("wishlist_book__price")
    if sort == '5':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by("wishlist_book__price").reverse()
    if sort == '6':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by("wishlist_book__year_of_publish")
    if sort == '7':
        book_list = Wishlist.objects.filter(wishlist_user=request.user).order_by(
            "wishlist_book__year_of_publish").reverse()

    author = Book.objects.values('author').distinct()

    return render(request, 'user_dashboard/wishlist.html', {'wishlists': book_list, 'authors': author})


def update_cart(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    book_list = request.session['book_list']
    print(book_list)
    return HttpResponse('ok')


def remove_cart(request, book_id):
    book_list_ids = request.session.get('book_list', False)
    book_list_ids = list(book_list_ids.replace('[', '').replace(']', '').split(","))
    book_list_ids = [int(x) for x in book_list_ids]

    book_list_ids.remove(book_id)
    print(book_list_ids)
    request.session['book_list'] = str(book_list_ids)
    return HttpResponse("OK")


def query_feedback(request):
    form = queryFeedbackForm()
    if request.method == 'POST':

        form = queryFeedbackForm(request.POST)
        if form.is_valid():
            # query_feedback = form.save(commit=False)
            subject = form.cleaned_data['query_feedback_subject']
            text = form.cleaned_data['query_feedback_text']
            QueryFeedback.objects.create(
                query_feedback_user_id=request.user,
                query_feedback_text=text,
                query_feedback_subject=subject
            ).save()
            return redirect('user_query_feedback_list')
        else:
            print('form.errors', form.errors)
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

            return render(request, 'user_dashboard/query_feedback.html', {'form': form})

    return render(request, 'user_dashboard/query_feedback.html', {'form': form})


def query_feedback_list(request):
    queries = QueryFeedback.objects.filter(
        query_feedback_user_id=request.user
    ).all()

    return render(request, 'user_dashboard/query_feedback_list.html', {'queries': queries})


def forget_password(request):
    return render(request, 'user_dashboard/forget_password.html',{})


def retrieve_password(request, email):
    user = User.objects.filter(email = email).first()
    if user:
        user.set_password('new_pass_123')
        user.save()
        return HttpResponse('Success')
    else:
        return HttpResponse('Email do not exists')
