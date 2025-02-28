from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "pub_date", "location", "category",
                  "is_published", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
