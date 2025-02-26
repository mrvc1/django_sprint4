from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Category, Post
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm


class ProfileView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['posts'] = Post.objects.filter(author=user)
        return context


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'registration/user.html', {'form': form})


def index(request):
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now, is_published=True, category__is_published=True
    ).order_by("-pub_date")[:5]
    context = {"page_obj": posts}
    return render(request, "blog/index.html", context)


def category_posts(request, category_slug):
    now = timezone.now()
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    posts = Post.objects.filter(
        category=category, is_published=True, pub_date__lte=now
    ).order_by("-pub_date")

    context = {"category": category, "posts": posts}
    return render(request, "blog/category.html", context)


def post_detail(request, id):
    now = timezone.now()
    post = get_object_or_404(
        Post, pk=id, is_published=True, pub_date__lte=now,
        category__is_published=True
    )

    context = {"post": post}
    return render(request, "blog/detail.html", context)
