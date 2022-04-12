from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm, UserEditForm
from .models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'blog/account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = RegisterForm()
    return render(request,
                  'blog/account/register.html',
                  {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/account/login.html', {'form': form})


@login_required
def dashboard(request):
    
    object_list = Post.objects.filter(author=request.user)
    
    paginator = Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
   
    return render(request,'blog/account/dashboard.html',{'section':'dashboard','page':page,'posts': posts}) 
    

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, instance=request.user,data=request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request,
                          'blog/account/register_done.html',
                          {'new_user': request.user})
    else:
        user_form = RegisterForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,
                  'blog/account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

