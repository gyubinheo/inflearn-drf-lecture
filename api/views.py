from rest_framework import generics, views, pagination
from rest_framework.response import Response

from .serializers import (
    PostListSerializer,
    PostDetailSerialzer,
    CommentSerializer,
    PostLikeSerializer,
    CateTagSerializer,
)
from .models import Post, Comment, Category, Tag


class PostPagination(pagination.PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(
            {
                "postList": data,
                "pageCnt": self.page.paginator.num_pages,
                "curPage": self.page.number,
            }
        )


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": None, "format": self.format_kwarg, "view": self}


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerialzer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            prevInstance = instance.get_previous_by_update_dt()
        except instance.DoesNotExist:
            prevInstance = None
        try:
            nextInstance = instance.get_next_by_update_dt()
        except instance.DoesNotExist:
            nextInstance = None
        commentList = instance.comment_set.all()
        data = {
            "post": instance,
            "prevPost": prevInstance,
            "nextPost": nextInstance,
            "commentList": commentList,
        }
        serializer = self.get_serializer(instance=data)
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": None, "format": self.format_kwarg, "view": self}


class PostLikeAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = {"like": instance.like + 1}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data["like"])


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CateTagAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()
        data = {
            "cateList": cateList,
            "tagList": tagList,
        }

        serializer = CateTagSerializer(instance=data)
        return Response(serializer.data)
