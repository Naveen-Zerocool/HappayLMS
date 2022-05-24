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

    @staticmethod
    def create_category(name):
        """
        Used to create a new category based on name. Slug will be auto populated on save
        :param name: str
        :return: Category instance
        """
        return Category.objects.create(name=name)

    @staticmethod
    def get_category_by_name(name):
        """
        Get category by name. We are filtering slug after doing slugify on name to avoid duplicates
        example: "science fiction" and "Science    Fiction  " will have same slugs and which will be a duplicate for us
        :param name: str
        :return: Category instance
        """
        return Category.objects.filter(slug=slugify(name)).first()

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"


class Author(GlobalBaseModel):
    name = models.CharField(max_length=150, unique=True, help_text="Author name")
    phone_number = PhoneNumberField(null=True, blank=True, help_text="Author phone number")
    birth_date = models.DateField(null=True, blank=True, help_text="Author birth date")
    death_date = models.DateField(null=True, blank=True, help_text="Author death date")

    def __str__(self):
        return self.name

    @staticmethod
    def get_author_by_name(name):
        """
        Used to fetch author by name
        :param name: str
        :return: Author instance or None
        """
        return Author.objects.filter(name__iexact=name).first()

    @staticmethod
    def create_author(name, phone_number=None, birth_date=None, death_date=None):
        """
        Used to create a new author
        :param name: str
        :param phone_number: str
        :param birth_date: str (date)
        :param death_date: str (date)
        :return: Author instance
        """
        return Author.objects.create(name=name, phone_number=phone_number,
                                     birth_date=birth_date, death_date=death_date)

    class Meta(GlobalBaseModel.Meta):
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "authors"


class Book(GlobalBaseModel):
    slug = models.SlugField(unique=True, blank=True)
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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Book, self).save(force_insert=force_insert, force_update=force_update,
                               using=using, update_fields=update_fields)

    @staticmethod
    def get_book_by_title_and_author(title, author):
        """
        Get book by name. We are filtering slug after doing slugify on name to avoid duplicates
        example: "science fiction" and "Science    Fiction  " will have same slugs and which will be a duplicate for us
        :param title: str
        :param author: Author
        :return: Book instance
        """
        return Book.objects.filter(slug=slugify(title), author=author).first()

    @staticmethod
    def add_book(title, author, category, publisher_name, published_date, price, units_sold):
        """
        Used to add a book
        :param title: str
        :param author: Author
        :param category: Category
        :param publisher_name: str
        :param published_date: date
        :param price: float
        :param units_sold: int
        :return: Book instance
        """
        return Book.objects.create(title=title, author=author, category=category, publisher_name=publisher_name,
                                   published_date=published_date, price=price, units_sold=units_sold)

    class Meta(GlobalBaseModel.Meta):
        unique_together = ["slug", "author_id"]
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "books"
