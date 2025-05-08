from django import forms
from .models import Tag, Comment, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    

class FilterForm(forms.Form):
  filter = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label='Select a Fiter Tag')


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('comment',)
    
  
class PostForm(forms.ModelForm):
  file = forms.FileField(required=False)
  
  class Meta:
    model = Post
    fields = ['title', 'body', 'tags',]
    widgets = { 'body': forms.Textarea(attrs={'id': 'id_content'})}
    