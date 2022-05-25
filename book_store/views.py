from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from HappayLMS.base_api_views import AuthenticatedAPIView
from HappayLMS.standard_responses import StandardResponse
from HappayLMS.utils import required_params
from book_store.models import Author, Category, Book
from book_store.serializers import AuthorSerializer, CategorySerializer, BookSerializer
from book_store.utils import validate_phone_number, validate_date, validate_data, convert_string_to_bool


class AuthorView(AuthenticatedAPIView, LimitOffsetPagination):

    def get(self, request, author_id=None):
        total_count = None
        if author_id:
            author = Author.objects.filter(pk=author_id).first()
            serialized_data = AuthorSerializer(author).data
            message = "Successfully returned author details"
        else:
            authors = Author.objects.all()
            authors = self.paginate_queryset(authors, request, view=self)
            total_count = Author.objects.count()
            serialized_data = AuthorSerializer(authors, many=True).data
            message = "Successfully returned all author details"
        return StandardResponse(response_data=serialized_data, total_count=total_count, message=message)

    @required_params(params=["name"])
    def post(self, request):
        data = request.data
        error = {}
        name = data.get("name")
        print(validate_data(data.get("phone_number"), validate_phone_number))
        phone_number, error_message = validate_data(data.get("phone_number"), validate_phone_number)
        if error_message:
            error.update({"phone_number": error_message})
        birth_date, error_message = validate_data(data.get("birth_date"), validate_date)
        if error_message:
            error.update({"birth_date": error_message})
        death_date, error_message = validate_data(data.get("death_date"), validate_date)
        if error_message:
            error.update({"death_date": error_message})
        if Author.get_author_by_name(name=name):
            error.update({"name": "Author with same name already exits, add some identifier for differencing authors"})
        if error:
            return StandardResponse(response_data={}, error=error, http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Failed to add author")

        author = Author.create_author(name=name, phone_number=phone_number,
                                      birth_date=birth_date, death_date=death_date)
        serialized_data = AuthorSerializer(author)
        return StandardResponse(response_data=serialized_data.data,
                                message="Added author details successfully")


class CategoryView(AuthenticatedAPIView, LimitOffsetPagination):

    def get(self, request, category_id=None):
        total_count = None
        if category_id:
            category = Category.objects.filter(pk=category_id).first()
            serialized_data = CategorySerializer(category).data
            message = "Successfully returned category details"
        else:
            categories = Category.objects.all()
            categories = self.paginate_queryset(categories, request, view=self)
            total_count = Category.objects.count()
            serialized_data = CategorySerializer(categories, many=True).data
            message = "Successfully returned all category details"
        return StandardResponse(response_data=serialized_data, total_count=total_count, message=message)

    @required_params(params=["name"])
    def post(self, request):
        data = request.data
        name = data.get("name")
        if Category.get_category_by_name(name=name):
            return StandardResponse(response_data={},
                                    error={"name": "Category with same name already exits"},
                                    http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Failed to add category")

        category = Category.create_category(name=name)
        serialized_data = CategorySerializer(category)
        return StandardResponse(response_data=serialized_data.data,
                                message="Added category successfully")


class BookSearchView(AuthenticatedAPIView, LimitOffsetPagination):

    def get(self, request):
        author_id = request.query_params.get("author_id")
        category_id = request.query_params.get("category_id")
        query_text = request.query_params.get("query_text")
        most_sold = request.query_params.get("most_sold")
        most_sold = convert_string_to_bool(str_=most_sold)
        total_count = 0
        if most_sold and query_text:
            return StandardResponse(
                response_data={}, error={
                    "most_sold": "Can fetch most sold only based Author or Category, remove query text"},
                http_status=status.HTTP_400_BAD_REQUEST,
                message="Error while searching for books"
            )
        if most_sold and not (category_id or author_id):
            return StandardResponse(response_data={},
                                    error={"most_sold": f"Author or Category is required to get most sold book"},
                                    http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Error while searching for books")
        books = Book.objects.none()
        if author_id:
            author = Author.objects.filter(pk=author_id).first()
            if not author:
                return StandardResponse(response_data={}, error={"author_id": f"Author not found with ID {author_id}"},
                                        http_status=status.HTTP_400_BAD_REQUEST,
                                        message="Error while searching for books")

        if category_id:
            category = Category.objects.filter(pk=category_id).first()
            if not category:
                return StandardResponse(response_data={},
                                        error={"category_id": f"Category not found with ID {category_id}"},
                                        http_status=status.HTTP_400_BAD_REQUEST,
                                        message="Error while searching for books")

        if author_id:
            books = Book.objects.filter(author_id=author_id)
        if category_id:
            if books:
                books = books.filter(category_id=category_id)
            else:
                books = Book.objects.filter(category_id=category_id)
        if query_text:
            if books:
                books = books.filter(Q(title__icontains=query_text) | Q(author__name__icontains=query_text))
            else:
                books = Book.objects.filter(Q(title__icontains=query_text) | Q(author__name__icontains=query_text))
        if most_sold:
            book = books.filter(units_sold__gte=1).order_by('-units_sold').first()
            if not book:
                return StandardResponse(response_data={}, message="There are no books sold in given criteria")
            serialized_data = BookSerializer(book).data
            message = "Successfully fetched most sold book"
        else:
            total_count = books.count() if books else 0
            books = self.paginate_queryset(books, request, view=self)
            serialized_data = BookSerializer(books, many=True).data
            message = "Successfully searched all books"
        return StandardResponse(response_data=serialized_data, total_count=total_count, message=message)


class BookView(AuthenticatedAPIView):

    @required_params(params=["title", "author_id", "category_id", "publisher_name", "published_date", "price"])
    def post(self, request):
        data = request.data
        title = data.get("title")
        author_id = data.get("author_id")
        category_id = data.get("category_id")
        publisher_name = data.get("publisher_name")
        published_date, error_message = validate_data(data.get("published_date"), validate_date, mandatory=True)
        price = float(data.get("price"))
        units_sold = data.get("units_sold")
        errors = {}

        if not title:
            errors.update({"title": "Title of book is required"})

        if not publisher_name:
            errors.update({"publisher_name": "Publisher Name is required"})

        if error_message:
            errors.update({"published_date": error_message})

        author = Author.objects.filter(pk=author_id).first()
        if not author:
            errors.update({"author_id": f"Author not found with ID {author_id}"})

        category = Category.objects.filter(pk=category_id).first()
        if not category:
            errors.update({"category_id": f"Category not found with ID {category_id}"})

        if Book.get_book_by_title_and_author(title=title, author=author):
            errors.update({"title": "Book exists with same name and author"})

        if price <= 0:
            errors.update({"price": "Price for the book should be more than 0"})

        if errors:
            return StandardResponse(response_data={}, error=errors, http_status=status.HTTP_400_BAD_REQUEST,
                                    message="Error while adding a book")

        book = Book.add_book(title=title, author=author, category=category,
                             publisher_name=publisher_name, published_date=published_date, price=price,
                             units_sold=units_sold)
        serialized_data = BookSerializer(book).data
        message = "Successfully added a book"
        return StandardResponse(response_data=serialized_data, message=message)
