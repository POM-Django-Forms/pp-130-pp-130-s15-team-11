from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    list_filter = ('name', 'surname', 'patronymic')
    search_fields = ('name', 'surname', 'patronymic')

    def full_name(self, obj):
        parts = [obj.surname, obj.name]
        if obj.patronymic:
            parts.append(obj.patronymic)
        return ' '.join(parts)
    full_name.short_description = 'Full Name'
