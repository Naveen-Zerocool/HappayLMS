"""HappayLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from book_store import api_urls as book_store_api_urls
from auth import api_urls as auth_api_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Happay LMS API",
        default_version='v1',
        description="Happay LMI API can be used for multiple operations like adding a author,"
                    "book, category, searching, etc. All available API documentation are given below",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include(auth_api_urls)),
    path('api/v1/book-store/', include(book_store_api_urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
