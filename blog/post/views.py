from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, UserPrefer, no_of_views, ContactAdmin, BlogRequest
from .forms import create_new_post, contactAdminForm, blogRequestForm
from django.utils.text import slugify
from django.conf import settings
import datetime
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.contrib import messages
from urllib.parse import quote_plus
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.utils import timezone
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile
# class editBlog(UpdateView):
#     model = Post
#     fields = ['title', 'content', 'image', 'image_caption', 'tags']
#     template_name_suffix = '_update_form'


def handler404(request, exception = None):
    return render(request, 'errors/404.html', status=404)
def handler500(request):
    return render(request, 'errors/500.html', status=500)

@login_required
def create_post(request):
    if not (request.user.is_staff or request.user.is_superuser or request.user.groups.filter(name='BlogWriters').exists()):
        raise Http404
    form = create_new_post()
    if request.method == "POST":
        
        form = create_new_post(request.POST, request.FILES or None)
        if form.is_valid():
            form.cleaned_data['author'] = request.user
            a = Post.objects.create(**form.cleaned_data)
            no_of_views.objects.create(post = a, views = 0)
    context = {
        "form" : form
    }
    return render(request, "post/new_post.html", context)

def blogRequest(request, slug):
    #Blog Request
    rform = blogRequestForm(request.POST or None)
    if 'blog-request' in request.POST:
        if rform.is_valid():
            a = BlogRequest.objects.create(**rform.cleaned_data)
    return redirect('post-detail', slug = slug)

def contactAdmin(request):
    form = contactAdminForm()
    if request.method == "POST":
        form = contactAdminForm(request.POST)
        if form.is_valid():
            a = ContactAdmin.objects.create(**form.cleaned_data)
    context = {
        "form" : form,
        "page" : "Contact Us",
    }
    return render(request, "post/contact.html", context)

def aboutUs(request):
    context  = {
        "page" : "About Us",
    }
    return render(request, "post/about.html", context)

def view_post(request, slug):
    instance = get_object_or_404(Post, slug = slug)
    if instance.draft or instance.publish > timezone.now().date():
        if request.user is not instance.author:
            if not request.user.is_superuser:
                raise Http404
    categories = Post.objects.values('category').distinct()
    tags = Post.objects.values('tags').distinct()
    recent = Post.objects.all().order_by('-updated_on')[:3]
    category_list = []
    for i in categories:
        category_list.append(i['category'])
    tag_list = []
    for i in tags:
        a = (i['tags']).split(',')
        for j in a:
            tag_list.append(j)
    a = (instance.tags).split(',')
    query = no_of_views.objects.get(post = instance)
    if not instance.draft:
        query.views += 1
        query.save()

    
    #Comments
    comments = Comment.objects.filter_by_instance(instance)
    commentscount = comments.count()
    initial_data = {
        "content_type" : instance.get_content_type,
        "object_id" : instance.id,
    }
    form = CommentForm(request.POST or None, initial = initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model = c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    
    context = {
        "instance" : instance,
        "categ" : category_list,
        "tags" : list(set(tag_list)),
        "recent" : recent,
        'a' : a,
        'views' : query.views,
        "comments" : comments,
        "commentform" : form,
        "commentscount" : commentscount,
        "page" : "View Post",
    }
    return render(request, "post/detail_post.html", context)


def enlist_post(request):
    categories = Post.objects.values('category').distinct()
    tags = Post.objects.values('tags').distinct()
    recent = Post.objects.all().order_by('-updated_on')[:3]
    category_list = []
    for i in categories:
        category_list.append(i['category'])
    tag_list = []
    for i in tags:
        a = (i['tags']).split(',')
        for j in a:
            tag_list.append(j)
        
    cat = request.GET.get('cat')
    tag = request.GET.get('tag')
    searchq = request.GET.get('search')
    if cat:
        queryset = Post.objects.all().filter(category = cat).order_by('-created_on')
    elif tag:
        queryset = Post.objects.all().filter(tags__contains = tag).order_by('-created_on')
    elif searchq:
        queryset = Post.objects.all().filter(Q(content__icontains = searchq) | Q(title__icontains = searchq)).order_by('-created_on')
    else:
        queryset = Post.objects.all().order_by('-created_on')

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 16)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)


    context = {
        "posts" : queryset,
        "categ" : category_list,
        "tags" : list(set(tag_list)),
        "recent" : recent,
        'queryset': numbers,
        "page" : "All Posts",
    }
    return render(request, 'post/posts_list.html', context)

def home(request):
    
    
    queryset1 = Post.objects.all().order_by('-updated_on')[:10]
    queryset2 = Post.objects.all().order_by('-created_on')[:10]
    categories = Post.objects.values('category').distinct()
    tags = Post.objects.values('tags').distinct()
    recent = Post.objects.all().order_by('-updated_on')[:3]
    category_list = []
    for i in categories:
        category_list.append(i['category'])
    tag_list = []
    for i in tags:
        a = (i['tags']).split(',')
        for j in a:
            tag_list.append(j)
        
    context = {
        "updatedposts" : queryset1,
        "newposts" : queryset2,
        "categ" : category_list,
        "tags" : list(set(tag_list)),
        "recent" : recent,
        "page" : "Home",
    }
    return render(request, 'post/index.html', context)

# def register(request):
#     return render(request, 'post/login.html')

@login_required
def delete_post(request, slug = None):
    instance = get_object_or_404(Post, slug = slug)
    if not (instance.author == request.user or request.user.is_superuser):
        raise 404
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('post-list')

@login_required
def update_post(request, slug = None):
    instance = get_object_or_404(Post, slug = slug)
    if instance.author.id == request.user.id or request.user.is_superuser:
        
        form = create_new_post(request.POST or None, request.FILES or None, instance = instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('post-list')
        image_url = instance.image
        context = {
            "instance" : instance,
            "form" : form,
            'imgurl' : image_url,
        }
    else:
        raise Http404
    

    return render(request, "post/update_post.html", context)



@login_required
def like(request, id = None):
    q = request.GET.get('q')
    postQuery = get_object_or_404(Post, id = id)
    try:
        query = UserPrefer.objects.filter(Post = postQuery, user = request.user )
        if query.count() == 0:
            UserPrefer.objects.create(Post = postQuery, value = q, user = request.user)
            postQuery.likes += 1
            
        else:
            query.delete()
            postQuery.likes -= 1
        print(query.count())
            
    except UserPrefer.DoesNotExist:
        postQuery.likes += 1
        UserPrefer.objects.create(Post = postQuery, value = q, user = request.user)
        
            

    postQuery.save()
    
    redirect_to = '/view/'+ postQuery.slug

    return HttpResponseRedirect(redirect_to)
    

def authorProfile(request, id = None):
    username = get_object_or_404(User, id = id)
    a = get_object_or_404(UserProfile, user = username)
    if a.profileDetailsVisible != 1:
        raise Http404
    profilePic, coverPic = a.profilePic, a.coverPic
    profile = UserProfile.objects.get(user = username)
    context = {
        'profile' : profile,
        'pp'     : profilePic,
        'cp'     : coverPic,
        "page"   : "Author's Profile",
    }
    return render(request, 'post/authorProfile.html', context)