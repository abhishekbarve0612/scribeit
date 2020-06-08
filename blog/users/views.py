from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group 
from users.forms import UserForm, EditProfileForm, ProfileForm
from .tokens import account_activation_token  
from django.core.mail import EmailMessage
from  post.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile


def logmeout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def managePosts(request):
    username = request.user
    q = Post.objects.filter(author = username)
    context = {
        'posts' : q,
    }
    return render(request, 'users/managePosts.html', context)

def adminHome(request):
    username = request.user
    if username.is_superuser:
        query = Post.objects.all()
    else:
        query = Post.objects.filter(author = username)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(query, 16)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    context = {
        'posts' : numbers,
    }

    return render(request, 'users/adminHome.html', context)

def register(request): 
    if request.method == 'POST':
        form = UserForm(request.POST)  
        # print(form.errors.as_data())  
        if form.is_valid():  
            user = form.save(commit=False)  
            user.is_active = False  
            pwd = form.cleaned_data['password']
            user.set_password(pwd)
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Activate your account.'  
            message = render_to_string('users/activatemail.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.id)),  
                'token': account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = UserForm() 
    return render(request, 'users/registration.html', {'user_form': form})

def activate(request, uidb64, token):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('../../')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'users/login.html', {})

@login_required
def makeBloggers(request):
    name = request.user
    g = Group.objects.get(name='BlogWriters')
    g.user_set.add(name)
    return redirect('posts-home')
    
def userProfile(request):
    print(request.user.id)
    a = get_object_or_404(UserProfile, user = request.user)
    profilePic, coverPic = a.profilePic, a.coverPic
    profile = UserProfile.objects.get(user = request.user)
    context = {
        'profile' : profile,
        'pp'     : profilePic,
        'cp'     : coverPic,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.user.userprofile is None:
        user_profile = UserProfile(user=request.user)
        user_profile.save
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES or None, instance=request.user.userprofile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            contactPrivacy = request.POST.get('contactPrivacy')
            profilePrivacy = request.POST.get('profilePrivacy')
            gender         = request.POST.get('gender')
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.contactDetailsVisible = contactPrivacy
            custom_form.profileDetailsVisible = profilePrivacy
            custom_form.gender                = gender
            custom_form.save()
            return redirect('users:user-profile')
    a = get_object_or_404(UserProfile, user = request.user)
    profilePic, coverPic = a.profilePic, a.coverPic
    form = EditProfileForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.userprofile)
    # args.update(csrf(request))
    context = {
        'form'   : profile_form,
        'myform' : form,
        'pp'     : profilePic,
        'cp'     : coverPic,
        'a'      : a,
    }
    return render(request, 'users/editprofile.html', context)


