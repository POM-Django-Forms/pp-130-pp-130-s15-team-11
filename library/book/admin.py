from django.contrib import admin
from .models import Book
from author.models import Author
from django.utils.html import format_html

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'display_authors', 'image')
    list_filter = ('id', 'name', 'authors')
    search_fields = ('name', 'authors__name')

    fieldsets = (
        ('Static Data', {
            'fields': ('name', 'description', 'count', 'authors'),
            'description': 'Data that does not change',
        }),
        ('Dynamic Data', {
            'fields': ('image',),
            'description': 'Data that may change',
        }),
    )

    def display_authors(self, obj):
        return ", ".join(author.name for author in obj.authors.all())
    display_authors.short_description = 'Authors'


    def image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "-"
    image.allow_tags = True
    image.short_description = 'Cover'