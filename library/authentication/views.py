import time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm

User = get_user_model()

def login_view(request):
    error = None
    if request.method == 'POST':
        if 'guest' in request.POST:
            return redirect('guest')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                if user.role == 1:
                    return redirect('profile', user_id=user.id)
                elif user.role == 2:
                    return redirect('guest')
                else:
                    return redirect('login')
            else:
                error = 'Wrong data!'
    else:
        form = UserLoginForm()
    return render(request, 'authentication/login.html', {'form': form, 'error': error})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 1
            user.is_active = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})


def librarians_view(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return redirect('guest')

    email_query = request.GET.get('email')
    if email_query:
        librarians = User.objects.filter(role=1, email__iexact=email_query)
    else:
        librarians = User.objects.filter(role=1)

    return render(request, 'authentication/librarians.html', {'librarians': librarians})


def guest_view(request):
    if not request.user.is_authenticated:
        unique_email = f'guest_{int(time.time())}@example.com'
        guest_user = User.objects.create_user(
            email=unique_email,
            password=User.objects.make_random_password(),
            first_name='Guest',
            last_name='User',
            middle_name='',
            role=2, 
            is_active=True
        )
        login(request, guest_user)
    elif request.user.role != 2:
        return redirect('profile', user_id=request.user.id)

    return render(request, 'authentication/guest.html')


def profile_view(request, user_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return redirect('guest')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('guest')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            profile = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                profile.set_password(password)
            profile.save()
            return redirect('profile', user_id=user.id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'authentication/profile.html', {'form': form, 'user': user})


def logout_view(request):
    logout(request)
    return redirect('login')