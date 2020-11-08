from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Register_Form(UserCreationForm):

	password1=forms.CharField(label="Password",widget=forms.PasswordInput(
		attrs={
			'class':"form-control"
		}
		))

	password2=forms.CharField(label="Password-confirmation",widget=forms.PasswordInput(
		attrs={
			'class':"form-control"
		}
		))

	class Meta:
		model=User
		fields=("password1","password2")