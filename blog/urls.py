from django.urls import path
from . import views
from .feed import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('add/', views.AddPost, name='addpost'),
    path('<int:post_id>/delete/',views.delpost, name='post_delete'),
    path('<int:post_id>/update/',views.update_post, name='post_update'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('like/', views.post_like, name='post_like'),
] 