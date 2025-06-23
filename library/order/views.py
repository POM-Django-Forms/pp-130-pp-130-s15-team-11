from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from book.models import Book
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from .forms import OrderForm

def is_librarian(user):
    return user.is_authenticated and user.role == 1

@login_required
@user_passes_test(is_librarian)
def all_orders_view(request):
    orders = Order.objects.select_related('book', 'user').all()
    return render(request, 'librarian/order_list.html', {'orders': orders})

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).select_related('book')
    return render(request, 'user/order_list.html', {'orders': orders})

@login_required
def create_order_view(request):
    error = None
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            book = order.book
            if book.count < 1:
                error = "Book is not available."
            else:
                order.user = request.user
                order.plated_end_at = timezone.now() + timedelta(weeks=2)
                order.save()
                book.count -= 1
                book.save()
                return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'user/create_order.html', {'form': form, 'error': error})

@login_required
@user_passes_test(is_librarian)
def close_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.end_at is None:
        order.update(end_at=timezone.now())
        order.save()
        order.book.count += 1
        order.book.save()
    return redirect('all_orders')
