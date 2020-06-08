from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from cloudinary.forms import CloudinaryFileField

from .models import UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
             'class' : "input-field",
             'label' : "Username",
            },
            ),
            required=True,
    )
    email = forms.EmailField( required = True),
    password = forms.CharField(widget=forms.PasswordInput(attrs={
             'class' : "input-field",
             'label' : "Password",
            },
            ),
            required=True,
            
    )
    class Meta():
        model = User
        fields = ('username','password','email')


class EditProfileForm(ModelForm):
        first_name = forms.CharField(widget = forms.TextInput(attrs={
             'class' : "validate",
             'label' : "First Name",
                'id' : "first-name"
            },
            ),
        )
        last_name = forms.CharField(widget = forms.TextInput(attrs={
             'class' : "validate",
             'label' : "Last Name",
                'id' : "last-name"
            },
            ),
        )
        email = forms.EmailField( widget = forms.EmailInput(attrs={
                'class' : "validate",
                'label' : "Email ID",
                'id' : "email"
        })),
        class Meta:
            model  = User
            fields = (
                    'email',
                    'first_name',
                    'last_name'
                    )
class ProfileForm(ModelForm):
        
        
        

        profilePic = CloudinaryFileField(
        options = {
            'crop': 'scale',
            'width': 500,
            'height': 500,
            'folder': 'blog-images',
        },
        required=False,
    )
        
        description = forms.CharField(widget=forms.Textarea(
                attrs = {
                        'id' : 'description',
                }
        ), required = False)
        address = forms.CharField(widget=forms.Textarea(
                attrs = {
                        'id' : 'address',
                        'data-length' : '60',
                }
        ), required = False)
        class Meta:
                model  = UserProfile
                fields = (
                'description', 'gender',
                'address',
                'mobileNumber', 'website', 'profilePic', 'coverPic',
                'contactDetailsVisible', 'profileDetailsVisible',
                'fav_music', 'fav_books', 'fav_movie', 
                'skills', 'interest',
                'facebook_url', 'linkedin_url', 'twitter_url', 'instagram_url',
                ) 