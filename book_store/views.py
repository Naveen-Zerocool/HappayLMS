from rest_framework.pagination import LimitOffsetPagination

from HappayLMS.base_api_views import GlobalAPIView
from HappayLMS.standard_responses import StandardResponse
from HappayLMS.utils import required_params
from book_store.models import Author, Category
from book_store.serializers import AuthorSerializer, CategorySerializer
from book_store.utils import validate_phone_number, validate_date, validate_data


class AuthorView(GlobalAPIView, LimitOffsetPagination):

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
            return StandardResponse(response_data={}, error=error, message="Failed to add author")

        author = Author.create_author(name=name, phone_number=phone_number,
                                      birth_date=birth_date, death_date=death_date)
        serialized_data = AuthorSerializer(author)
        return StandardResponse(response_data=serialized_data.data,
                                message="Added author details successfully")


class CategoryView(GlobalAPIView, LimitOffsetPagination):

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
                                    message="Failed to add category")

        category = Category.create_category(name=name)
        serialized_data = CategorySerializer(category)
        return StandardResponse(response_data=serialized_data.data,
                                message="Added category successfully")
