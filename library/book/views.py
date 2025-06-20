from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from author.models import Author
from order.models import Order
from .forms import BookForm

def is_librarian(user):
    return user.is_authenticated and user.role == 1

@login_required
def book_list_view(request):
    query = request.GET.get('q', '').strip()
    author_id = request.GET.get('author', '').strip()

    books = Book.objects.all()
    if query:
        books = books.filter(name__icontains=query)
    if author_id.isdigit():
        books = books.filter(authors__id=int(author_id))

    authors = Author.objects.all()
    template = 'librarian/book_list.html' if is_librarian(request.user) else 'user/book_list.html'

    return render(request, template, {
        'books': books.distinct(),
        'authors': authors,
        'query': query,
        'author_id': author_id,
    })

@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    template = 'librarian/book_detail.html' if is_librarian(request.user) else 'user/book_detail.html'
    return render(request, template, {'book': book})

@login_required
@user_passes_test(is_librarian)
def create_book_view(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('librarian_book_list')
    else:
        form = BookForm()
    return render(request, 'create_book.html', {'form': form})

@login_required
@user_passes_test(is_librarian)
def delete_book_view(request, book_id):
    book = Book.get_by_id(book_id)
    if book:
        Book.delete_by_id(book_id)
    return redirect('librarian_book_list')

@login_required
@user_passes_test(is_librarian)
def update_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('librarian_book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(is_librarian)
def user_books_view(request, user_id):
    orders = Order.objects.filter(user_id=user_id, end_at=None).select_related('book').prefetch_related('book__authors')
    books = [order.book for order in orders]
    return render(request, 'books_by_user.html', {'books': books})
