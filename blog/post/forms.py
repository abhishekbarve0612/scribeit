from django import forms
from .models import Post, ContactAdmin, BlogRequest
from cloudinary.forms import CloudinaryFileField

class contactAdminForm(forms.ModelForm):
    class Meta:
        model = ContactAdmin
        fields = ['name', 'emailid', 'subject', 'message']

class blogRequestForm(forms.ModelForm):
    class Meta:
        model = BlogRequest
        fields = ['author', 'userRequest']


class create_new_post(forms.ModelForm):
    category = forms.CharField()
    title = forms.CharField()
    image = CloudinaryFileField(
        options = {
            'crop': 'scale',
            'width': 500,
            'height': 500,
            'folder': 'blog-images',
        },
        required=False,
    )
    image_caption = forms.CharField(required=False,)
    tags = forms.CharField(widget = forms.TextInput(attrs={
            'data-role' : "tagsinput",
             'class' : "form-control bootstrap-tagsinput",
             'id' : "tags-multiple",
            },
            ),
            required=False,
    )
    publish = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image', 'image_caption', 'tags', 'draft', 'publish']