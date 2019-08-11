from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import SignUpForm, NewPost
from taggit.models import Tag
from taggit.managers import TaggableManager
from django.db.models import Count
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from .forms import PasswordReset
from django.contrib.auth.models import User


# create class views
class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


# Create your views here.
def homepage(request, tag_slug=None):
    object_list = Post.published.all()
    # editor = mark_safe(object_list.editor1)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'page': posts, 'posts': posts, 'tag': tag, })


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('list')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'page': posts, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'details.html', {'post': post, 'similar_posts': similar_posts})


def new_post(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            slug = slugify(form.cleaned_data['title'])
            post.slug = slug
            post.author = request.user
            post.publish = timezone.now()
            post.status = form.cleaned_data['status']
            post.save()
            tid = post.id
            post = Post.objects.get(id=tid)
            tagval = form.cleaned_data['tags'].split(',')
            for tag in tagval:
                post.tags.add(tag.strip())
            post.save()
            return redirect('list')
        else:
            return redirect('home')
    else:
        form = NewPost()
    return render(request, 'post_new.html', {'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})
