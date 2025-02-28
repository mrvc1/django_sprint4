from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<str:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('edit_profile/', views.ProfileEditView.as_view(),
         name='edit_profile'),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/<int:pk>/edit/", views.update_post, name="edit_post"),
    path("posts/<int:post_pk>/comment/", views.add_comment,
         name="add_comment"),
    path("posts/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("posts/<int:post_pk>/delete_comment/<int:comment_pk>/",
         views.delete_comment, name="delete_comment"),
    path("posts/<int:post_pk>/edit_comment/<int:comment_pk>/",
         views.update_comment, name="edit_comment"),
]
