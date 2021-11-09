import datetime
import json
import uuid

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from book_store.admin_dashboard.forms import book_form, register_form, user_mode_form, deal_voucher_form, \
    user_deal_voucher_form
from book_store.admin_dashboard.models import Book, Voucher, VoucherUser, Quiz, Deal, Cart, BookAudio
from book_store.user.models import User, Mode
from mailjet_rest import Client


@staff_member_required(login_url='/')
def index(request):
    books = Book.objects.all()
    users = User.objects.all()

    data = {
        'books': books,
        'users': users,
    }
    return render(request, 'dashboard/dashboard.html', data)


@csrf_exempt
@staff_member_required(login_url='/')
def add_book(request):
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

        year_of_publish = datetime.datetime(int(year_of_publish), month=1, day=1).date()
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
    return render(request, 'dashboard/add_book.html', {})
    # return HttpResponse('test')


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


@staff_member_required(login_url='/')
def list_book(request):
    books = Book.objects.all()
    data = {
        'books': books
    }
    return render(request, 'dashboard/book_list.html', data)


@staff_member_required(login_url='/')
def delete_book(request, book_id):
    Book.objects.filter(book_id=book_id).delete()
    print(book_id)
    return HttpResponse({'Success': 'True'})


@staff_member_required(login_url='/')
def add_user(request):
    if request.method == 'POST':
        form = register_form(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)

            code = uuid.uuid4().hex.upper()[0:6]

            Voucher.objects.create(description='Signup Voucher',
                                   credit=200, code=code).save()
            voucher = Voucher.objects.filter(
                voucher_id=Voucher.objects.filter(code=code).first().voucher_id
            ).first()

            VoucherUser.objects.create(voucher=voucher, user=user).save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))

    return render(request, 'dashboard/add_user.html', {'form': register_form()})


@staff_member_required(login_url='/')
def list_user(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})


@staff_member_required(login_url='/')
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


@staff_member_required(login_url='/')
def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return HttpResponse({'Success': 'True'})


@staff_member_required(login_url='/')
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


@staff_member_required(login_url='/')
def list_user_mode(request):
    modes = Mode.objects.all()
    return render(request, 'dashboard/mode_list.html', {'modes': modes})


@staff_member_required(login_url='/')
def delete_mode(request, mode_id):
    Mode.objects.filter(mode_id=mode_id).delete()
    return HttpResponse({'Success': 'True'})


@staff_member_required(login_url='/')
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


@staff_member_required(login_url='/')
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


@staff_member_required(login_url='/')
def list_deal_voucher(request):
    vouchers = Voucher.objects.all()
    return render(request, 'dashboard/deal_voucher_list.html', {'vouchers': vouchers})


@staff_member_required(login_url='/')
def edit_deal_voucher(request, deal_voucher_id):
    if request.method == 'POST':
        obj = get_object_or_404(Voucher, deal_voucher_id=deal_voucher_id)
        form = deal_voucher_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin-home')
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
    else:
        form = deal_voucher_form(instance=Voucher.objects.filter(deal_voucher_id=deal_voucher_id).first())

    return render(request, 'dashboard/edit_deal_voucher.html', {'form': form, 'deal_voucher_id': deal_voucher_id})


@staff_member_required(login_url='/')
def delete_deal_voucher(request, deal_voucher_id):
    Voucher.objects.filter(deal_voucher_id=deal_voucher_id).delete()
    return HttpResponse({'Success': 'True'})


@staff_member_required(login_url='/')
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


@staff_member_required(login_url='/')
def list_user_deal_voucher(request):
    vouchers = VoucherUser.objects.all()
    return render(request, 'dashboard/user_deal_voucher_list.html', {'vouchers': vouchers})


@staff_member_required(login_url='/')
def delete_user_deal_voucher(request, deal_voucher_user_id):
    VoucherUser.objects.filter(deal_voucher_user_id=deal_voucher_user_id).delete()
    return HttpResponse({'Success': 'True'})


@staff_member_required(login_url='/')
def admin_edit_user_deal_voucher(request, deal_voucher_user_id):
    if request.method == 'POST':
        obj = get_object_or_404(VoucherUser, deal_voucher_user_id=deal_voucher_user_id)
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
            instance=VoucherUser.objects.filter(deal_voucher_user_id=deal_voucher_user_id).first())

    return render(request, 'dashboard/edit_user_deal_voucher.html',
                  {'form': form, 'deal_voucher_user_id': deal_voucher_user_id})


@staff_member_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('/')


@staff_member_required(login_url='/')
def add_quiz(request):
    return render(request, 'dashboard/add_quiz.html', {'books': Book.objects.all()})


@staff_member_required(login_url='/')
def list_quiz(request):
    return render(request, 'dashboard/quiz_list.html', {'quizs': Quiz.objects.all()})


@staff_member_required(login_url='/')
def save_game(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        game_question_title = data['game_question_title']
        game_type = data['game_type']
        quiz = Quiz.objects.create(
            quiz_type='game-' + game_type,
            quiz_question_statement=game_question_title
        ).save()

    return HttpResponse(status=200)


@staff_member_required(login_url='/')
@ensure_csrf_cookie
def save_mcqs(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        question = data['question']
        option_1 = data['option_1']
        option_2 = data['option_2']
        option_3 = data['option_3']
        option_4 = data['option_4']
        mcq_answer = data['mcq_answer']
        mcq_book = list(map(int, data['mcq_book']))

        books = Book.objects.filter(book_id=mcq_book[0]).first()

        quiz = Quiz.objects.create(
            quiz_type='mcq',
            quiz_question_statement=question,
            quiz_option_1=option_1,
            quiz_option_2=option_2,
            quiz_option_3=option_3,
            quiz_option_4=option_4,
            quiz_answer=mcq_answer,
            quiz_book=books
        )
        quiz.save()
        # print(question, option_1, option_2, option_3, option_4)
    return HttpResponse(status=200)


@staff_member_required(login_url='/')
def save_question(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        question = data['question']
        answer = data['answer']
        question_book = data['question_book']

        quiz = Quiz.objects.create(
            quiz_type='QUESTION',
            quiz_question_statement=question,
            quiz_answer=answer,
            quiz_book=Book.objects.filter(book_id=question_book).first()
        ).save()

        print(question, answer)
    return HttpResponse(status=200)


def add_deal(request):
    books = Book.objects.all()
    return render(request, 'dashboard/add_deal.html', {'books': books})


def list_deal(request):
    deals = Deal.objects.all()
    return render(request, 'dashboard/deal_list.html', {'deals': deals})


def save_deal(request):
    if request.method == 'GET':
        data = json.loads(request.GET.dict()['data'])
        title = data['title']
        percentage = data['percentage']
        discounted_books = list(map(int, data['discounted_books']))
        valid_upto = data['valid_upto']
        books = Book.objects.filter(book_id__in=discounted_books)
        deal = Deal.objects.create()
        deal.deal_valid_upto = valid_upto
        deal.deal_percentage = percentage
        print(title)
        deal.deal_title = title
        [deal.deal_book.add(book) for book in books]
        deal.save()
    return HttpResponse('Success')


def delete_deal(request, deal_id):
    Deal.objects.filter(deal_id=deal_id).delete()
    return redirect('admin-list-deal')


def delete_quiz(request, quiz_id):
    Quiz.objects.filter(quiz_id=quiz_id).delete()
    return redirect('admin-list-deal')


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


def make_author_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    user.is_author = True
    user.save()
    return HttpResponse('Success')


def make_admin_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    user.is_admin = True
    user.is_staff = True

    user.save()
    return HttpResponse('Success')
