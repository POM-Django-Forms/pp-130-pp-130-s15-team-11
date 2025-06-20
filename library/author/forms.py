from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']
        labels = {
            'name': 'First Name',
            'surname': 'Last Name',
            'patronymic': 'Middle Name or Patronymic',
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['patronymic'].required = False
