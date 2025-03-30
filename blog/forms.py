from django import forms
from .models import Tag, Comment


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