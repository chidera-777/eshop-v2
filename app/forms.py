from django import forms
from .models import Newsletter

class NewsletterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args,**kwargs)
      self.fields['email'].label = ''
      
    class Meta:
      model = Newsletter
      fields = ['email']
      widgets = {
        'email': forms.TextInput(attrs={'placeholder': 'Your Email'}),
      }
      
    def clean_email(self):
        email = self.cleaned_data['email']
        if Newsletter.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A subscription for the email already exists')
        return email