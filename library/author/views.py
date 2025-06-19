from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Author

def is_librarian(user):
    return user.is_authenticated and user.role == 1

@login_required
@user_passes_test(is_librarian)
def author_list_view(request):
    authors = Author.get_all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if name and surname and patronymic:
            Author.create(name=name, surname=surname, patronymic=patronymic)
            return redirect('author_list')

    return render(request, 'author_list.html', {'authors': authors})

@login_required
@user_passes_test(is_librarian)
def create_author_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()
        
        if not patronymic:
            patronymic = None

        if name and surname:
            Author.create(name=name, surname=surname, patronymic=patronymic)
            return redirect('author_list')  

    return render(request, 'create_author.html')

@login_required
@user_passes_test(is_librarian)
def delete_author_view(request, author_id):
    author = Author.get_by_id(author_id)
    if author and not author.books.exists():
        Author.delete_by_id(author_id)
    return redirect('author_list')
