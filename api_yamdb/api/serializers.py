from rest_framework import serializers
from reviews.models import Category, Genre, Review, Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'score')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ("__all__")
        read_only_fields = ('title',)
