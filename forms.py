from django import forms
from django.contrib.auth.models import User
from blog.models import Comment, UserProfile, Entry


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("created", "author", "body",)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
        
class UserForm(forms.ModelForm):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    class Meta:
        model = UserProfile
        exclude = ('user',)

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        
class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=50)