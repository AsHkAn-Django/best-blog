from django import forms
from .models import Tag, Comment


class FilterForm(forms.Form):
  filter = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label='Select a Fiter Tag')

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('comment',)