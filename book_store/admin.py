from django.contrib import admin
from django.contrib.auth.models import Group

from book_store.models import Category, Author, Book


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)


admin.site.unregister(Group)
