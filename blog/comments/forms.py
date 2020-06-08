from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment
class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label = '', widget=forms.Textarea(attrs=
        {
            'cols' : 40,
            'rows' : 7,
            'class' : 'comment-text-area',
        }
    ))

    

    