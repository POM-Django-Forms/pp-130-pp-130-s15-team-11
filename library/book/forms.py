from django import forms
from .models import Book
from author.models import Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors', 'image']
        labels = {
            'name': 'Book Title',
            'description': 'Book Description',
            'count': 'Available Copies',
            'authors': 'Authors',
            'image': 'Book Cover Image',
        }
        widgets = {
            'authors': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False  
        self.fields['image'].required = False  
