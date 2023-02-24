from django.urls import path, include
from . import views


urlpatterns = [
    path("post/", views.PostListAPIView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostRetrieveAPIView.as_view(), name="post-detail"),
    path("post/<int:pk>/like/", views.PostLikeAPIView.as_view(), name="post-like"),
    path("comment/", views.CommentCreateAPIView.as_view(), name="comment-list"),
    path("catetag/", views.CateTagAPIView.as_view(), name="catetag"),
]
