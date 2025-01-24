from django import forms
from django.core.validators import EmailValidator
from .models import CustomUser

class UserUpdateForm(forms.ModelForm):
   email = forms.EmailField(
       widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
       validators=[EmailValidator()]
   )
   first_name = forms.CharField(
       widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})
   )
   last_name = forms.CharField(
       widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'})
   )

   class Meta:
       model = CustomUser
       fields = ['first_name', 'last_name', 'email']
       
       
# forms.py
class UserProfileUpdateForm(forms.ModelForm):
   profile_image = forms.ImageField(
       required=False,
       widget=forms.FileInput(attrs={'class': 'hidden', 'id': 'profile_image'})
   )
   first_name = forms.CharField(
       widget=forms.TextInput(attrs={'class': 'form-input'})
   )
   last_name = forms.CharField(
       widget=forms.TextInput(attrs={'class': 'form-input'}) 
   )
   email = forms.EmailField(
       widget=forms.EmailInput(attrs={'class': 'form-input'})
   )

   class Meta:
       model = CustomUser
       fields = ['profile_image', 'first_name', 'last_name', 'email']