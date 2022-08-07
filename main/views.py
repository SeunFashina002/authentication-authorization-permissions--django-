from multiprocessing import context
from django.shortcuts import redirect, render
from . forms import RegisterForm, PostForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post
from django.contrib.auth.models import User, Group
# Create your views here.


@login_required(login_url='/login')
def index(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            
            if post and (post.author == request.user or request.user.has_perm('main.delete_post') ):
                post.delete()

        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
                



    context = {
        'posts' : posts
    }
    return render(request, 'main/index.html', context)


@permission_required('main.add_post', login_url='/login', raise_exception=True)
@login_required(login_url = '/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    context = {
        'form' : form
    }

    return render(request, 'main/create_post.html', context)

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
            
    else:
        form = RegisterForm()

    context = {
        'form' : form
    }
    return render(request, 'registration/sign_up.html', context)