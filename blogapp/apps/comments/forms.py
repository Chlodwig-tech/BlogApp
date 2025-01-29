from django import forms
from datetime import datetime

from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Dodaj komentarz', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    parent  = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'hidden', 'value': -1}))
    #<input type="hidden" name="parent" value="-1">
    class Meta:
        model = Comment
        fields = (
            'content',
        )

    def save(self, author, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.author = author
        
        comment.publish_date = datetime.now()
        if commit:
            comment.save()

        return comment