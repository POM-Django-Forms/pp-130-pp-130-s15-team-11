from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Author
from .forms import AuthorForm

def is_librarian(user):
    return user.is_authenticated and user.role == 1

@login_required
@user_passes_test(is_librarian)
def author_list_view(request):
    authors = Author.get_all()
    return render(request, 'author_list.html', {'authors': authors})

@login_required
@user_passes_test(is_librarian)
def create_author_view(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'create_author.html', {'form': form})
    
@login_required
@user_passes_test(is_librarian)
def update_author_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'update_author.html', {'form': form, 'author': author})

@login_required
@user_passes_test(is_librarian)
def delete_author_view(request, author_id):
    author = Author.get_by_id(author_id)
    if author and not author.books.exists():
        Author.delete_by_id(author_id)
    return redirect('author_list')
