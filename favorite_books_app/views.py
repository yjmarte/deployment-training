from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import *
from .forms import *
import bcrypt

def index(request):
    if 'user_id' in request.session:
        redirect('/books')
    r_form = RegistrationForm()
    l_form = LoginForm()
    
    context = {
        'r_form': r_form,
        'l_form': l_form,
    }
    
    return render(request, 'index.html', context)

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for k, v in errors.items():
                messages.error(request, v, extra_tags='registration')
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.password = pw_hash
                user.save()
                request.session['user_id'] = user.id
                return redirect('/books')
    else:
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for k, v in errors.items():
            messages.error(request, v, extra_tags='login')
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/books')

def books(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'form': BookForm(),
            'all_books': Book.objects.all(),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'books.html', context)

def favorited(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_books': Book.objects.all(),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'favorited.html', context)

def create(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for k, v in errors.items():
            messages.error(request, v, extra_tags='book')
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session["user_id"])
        form = BookForm(data=request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.poster = user
            book.save()
        # Book uploader automatically favorites the book
        user.favorited_books.add(book)

        return redirect(f'/books/{book.id}')

def retrieve(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.poster.id != request.session['user_id']:
        form = BookForm()
        fields = list(form)
        p1, p2 = fields[:1], fields[1:]
    else:
        i = get_object_or_404(Book, pk=book_id)
        form = BookForm(instance=i)
        fields = list(form)
        p1, p2 = fields[:1], fields[1:]
    context = {
        'p1': p1,
        'p2': p2,
        'book': Book.objects.get(id=book_id),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "book.html", context)

def update(request, book_id):
    i = Book.objects.get(id=book_id)
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for k, v in errors.items():
            messages.error(request, v, extra_tags='book')
        return redirect(f'/books/{book_id}')
    elif request.method == 'POST':
        form = BookForm(request.POST, instance=i)
        if form.is_valid():
            book = form.save()
            return redirect(f"/books/{book_id}")
    else:
        return redirect('/books')

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.add(book)

    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.remove(book)

    return redirect(f'/books/{book_id}')

def logout(request):
    request.session.flush()

    return redirect('/')