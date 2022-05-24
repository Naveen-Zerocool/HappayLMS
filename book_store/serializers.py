from rest_framework import serializers

from book_store.models import Author, Category, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['pk', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"pk": obj.author_id, "name": obj.author.name} if obj.author_id else {}

    def get_category(self, obj):
        return {"pk": obj.category_id, "name": obj.category.name} if obj.category_id else {}

    class Meta:
        model = Book
        fields = ["pk", "title", "author", "category", "publisher_name", "published_date", "price", "units_sold"]
