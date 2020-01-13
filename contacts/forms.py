from django import forms

from .models import ContactMessages

class ContactMessagesForm(forms.ModelForm):
    class Meta:
        model = ContactMessages
        fields = ('message_text','email', 'pwd')
        widgets = {'pwd': forms.PasswordInput()}