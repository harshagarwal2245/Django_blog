from django import forms
from .models import Post, Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','snippet','status')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class SearchForm(forms.Form):
    query = forms.CharField()