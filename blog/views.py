from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm,PostAddForm,CommentForm,SearchForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.text import slugify
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count
from django.contrib.flatpages.models import FlatPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
#new try:


def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    
    
    paginator = Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
   
    return render(request, 'blog/post/list.html', {'page':page,'posts': posts,'tag':tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST': 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    """ 
    Retriving similat post using tags
    """
    post_tag_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,'comments': comments,'new_comment': new_comment,'comment_form': comment_form,'similar_posts':similar_posts})


def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'agarwalharsh244@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

def is_journalist(user):
    return user.is_staff or user.is_superuser




def AddPost(request):
    if request.method=='POST':
        form=PostAddForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.slug=slugify(form.cleaned_data['title'])
            print(form.cleaned_data["header"])
            if is_journalist(request.user):
                post.save()
                return render(request,'blog/post/post_added.html',{'post':post})
            else:
                return render(request,'blog/post/not_allowed.html')
    else:
        form=PostAddForm()
    return render(request,'blog/post/add.html',{'form':form}) 


def delpost(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if is_journalist(request.user):
        post.delete()
        return render(request,'blog/post/post_deleted.html',{'post':post})
    else:
        return render(request,'blog/post/not_allowed.html')


def update_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if is_journalist(request.user):
        if request.method=='POST':
            form=PostAddForm(request.POST,instance=post,files=request.FILES)
            if form.is_valid():
                post=form.save(commit=False)
                post.author=request.user
                post.slug=slugify(form.cleaned_data['title'])
                post.save()
                return render(request,'blog/post/post_updated.html',{'post':post})
        else:
            form=PostAddForm(instance=post)
        return render(request,'blog/post/update.html',{'form':form})


@login_required
@require_POST
def post_like(request):
    """ Function used to like the post and maintain the record of it"""
    post_id=request.POST.get('id')
    action=request.POST.get('action')
    print(post_id,action)
    if post_id and action:
        try:
            post=Post.objects.get(id=post_id)
            if action=='like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})
