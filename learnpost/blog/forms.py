from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
          'content': forms.Textarea(attrs={'rows':2, 'cols':40, 'placeholder':"Enter your comment"}),
        }