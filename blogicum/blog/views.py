from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from .models import Category, Post, Comment
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, CommentUpdateForm, ProfileEditForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count


class ProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = (
            Post.objects.filter(author=self.object)
            .order_by('-created_at'))
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect("blog:post_detail", pk=post.pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/create.html",
                  {"form": form, "post": post})


@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", id=post.pk)
    else:
        form = CommentForm()
    return render(request, "includes/comments.html",
                  {"form": form, "post": post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect("blog:post_detail", id=post.pk)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html",
                  {"post": post})


@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.author:
        return redirect("blog:post_detail", id=post_pk)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", id=post_pk)
    return render(request, "blog/comment.html",
                  {"comment": comment})


@login_required
def update_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        return redirect("blog:post_detail", id=post.pk)

    if request.method == "POST":
        form = CommentUpdateForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", id=post.pk)
    else:
        form = CommentUpdateForm(instance=comment)

    return render(request, "blog/comment.html",
                  {"form": form, "post": post, "comment": comment})


def index(request):
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now, is_published=True, category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by("-pub_date")[:5]
    context = {"page_obj": posts}
    return render(request, "blog/index.html", context)


def category_posts(request, category_slug):
    now = timezone.now()
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = Post.objects.filter(
        category=category, is_published=True, pub_date__lte=now
    ).order_by("-pub_date")

    context = {"category": category, "page_obj": posts}
    return render(request, "blog/category.html", context)


def post_detail(request, id):
    now = timezone.now()
    post = get_object_or_404(
        Post,
        pk=id,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        'form': form,
    }
    return render(request, "blog/detail.html", context)
