from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_book', 'created_at', 'plated_end_at', 'end_at', 'is_returned')
    list_filter = ('created_at', 'plated_end_at', 'end_at', 'book', 'user')
    search_fields = ('user__email', 'book__name')
    readonly_fields = ('created_at',)

    def get_user(self, obj):
        return f'{obj.user.email} (id={obj.user.id})'
    get_user.short_description = 'User'

    def get_book(self, obj):
        return f'{obj.book.name} (id={obj.book.id})'
    get_book.short_description = 'Book'

    def is_returned(self, obj):
        return obj.end_at is not None
    is_returned.boolean = True
    is_returned.short_description = 'Returned'
