from django import forms
from .models import post,profile,Comments
from django.contrib.auth.models import User
class postform(forms.ModelForm):
	description = forms.CharField(label='Description ',
		widget=forms.Textarea(attrs=
			{
			'class':'reg_form',
			'placeholder':'Enter Your Comments..',
			'rows':4,
			'cols':50,
			}
			))
	class Meta:
		model = post
		fields = (
			'title',
			'description',
			'status',
			'restrict_comments'
			)

class post_editform(forms.ModelForm):
	description = forms.CharField(label='Description ',
		widget=forms.Textarea(attrs=
			{
			'class':'reg_form',
			'placeholder':'Enter Your Comments..',
			'rows':4,
			'cols':50,
			}
			))
	class Meta:
		model = post
		fields = (
			'title',
			'description',
			'status',
			'restrict_comments'
			)

class loginform(forms.Form):
	username = forms.CharField(label=' User Name  ')
	password = forms.CharField(label=' Password  ',widget=forms.PasswordInput)

class userregistrationform(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)

class userform(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)

class profileform(forms.ModelForm):
	class Meta:
		model = profile
		exclude = ('user',)

class commentsform(forms.ModelForm):
	content = forms.CharField(label='',
		widget=forms.Textarea(attrs=
			{
			'class':'reply_box',
			'placeholder':'Enter Your Comments..',
			'rows':2,
			'cols':40,
			}
			))
	class Meta:
		model = Comments
		fields = (
			'content',)
		