from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from HappayLMS.base_model import GlobalBaseModel


class Category(GlobalBaseModel):
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=150, help_text="Category name")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(Category, self).save(force_insert=force_insert, force_update=force_update,
                                   using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"


class Author(GlobalBaseModel):
    name = models.CharField(max_length=150, help_text="Author name")
    phone_number = PhoneNumberField(null=True, blank=True, help_text="Author phone number")
    birth_date = models.DateField(null=True, blank=True, help_text="Author birth date")
    death_date = models.DateField(null=True, blank=True, help_text="Author death date")

    def __str__(self):
        return self.name

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "authors"


class Book(GlobalBaseModel):
    title = models.TextField(help_text="Name of the Book")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books",
                               help_text="Author of the book")
    publisher_name = models.TextField(help_text="Name of the publisher")
    published_date = models.DateField(help_text="Book published date")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books",
                                 help_text="Book category")
    price = models.FloatField(help_text="Price of the book", validators=[MinValueValidator(1.0)])
    units_sold = models.PositiveSmallIntegerField(help_text="Number of books sold", default=0, db_index=True)

    def __str__(self):
        title = f"{self.title}"
        if self.author_id:
            title += f" - {self.author.name}"
        if self.category_id:
            title += f" - {self.category.name}"
        return title

    class Meta(GlobalBaseModel.Meta):
        unique_together = ["title", "author_id"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "books"
