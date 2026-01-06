from django import forms
from .models import Tag, Comment, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class FilterForm(forms.Form):
    filter = forms.ModelChoiceField(
        queryset=Tag.objects.all(), required=False, label="Select a Fiter Tag"
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)


class PostForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ["title", "body", "tags"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your post title",
                    "id": "id_title",
                }
            ),
            "body": forms.Textarea(attrs={"class": "form-control", "id": "id_content"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
