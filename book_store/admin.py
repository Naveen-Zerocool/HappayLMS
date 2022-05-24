from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

from book_store.models import Category, Author, Book


class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author__name', 'category__title', 'publisher_name']
    list_display = ['title', 'author', 'category']
    list_filter = ['category__name']
    date_hierarchy = 'published_date'
    autocomplete_fields = ['author', 'category']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)


admin.site.unregister(Group)


AdminSite.site_header = "Happay LMS Admin"
AdminSite.site_title = "Happay LMS Admin"
AdminSite.site_url = None
AdminSite.index_title = "Happay LMS Administration"
