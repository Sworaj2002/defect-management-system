from django import forms
from django.contrib.auth.models import User
from .models import UserData
from django_recaptcha.fields import ReCaptchaField

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']
        # fields = '__all__'
class UserpData(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['Door_no','Street','City','State',"Zipcode",'Profile_pic']
        captcha = ReCaptchaField()
class Updateform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
class UpdateprofileForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['Door_no','Street','City','State',"Zipcode",'Profile_pic']

class ResetPasswordForm(forms.Form):
    username= forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100,widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if username:
            try:
                User.objects.get(username=username)
                if password != confirm_password:
                    raise forms.ValidationError("Password didnot match")
            except:
                raise forms.ValidationError("Username Doesnot Exit")
            


