from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone as tz
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(date_published__lte=tz.now()).order_by('-date_published')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            # post.date_published = tz.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = tz.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
def post_draft_list(request):
    posts = Post.objects.filter(date_published__isnull = True).order_by('date_published')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post= post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.date_published = tz.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})
