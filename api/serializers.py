from rest_framework import serializers
from .models import Post, Comment


class PostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Post
        fields = ["id", "title", "image", "like", "category"]


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["like"]


class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        exclude = ["create_dt"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())


class PostSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title"]


class CommentSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "update_dt"]


class PostDetailSerialzer(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSubSerializer()
    nextPost = PostSubSerializer()
    commentList = CommentSubSerializer(many=True)
