"""site_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from blog.views import LoginView, logout_request


schema_view = get_schema_view(
   openapi.Info(
      title='Site Documentation',
      default_version='v1',
      description='API description',
      terms_of_service='https://www.google.com/policies/terms/',
   ),
   public=False,
   permission_classes=(IsAuthenticated,),
   authentication_classes=(SessionAuthentication,)
)


urlpatterns = [
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        login_required(schema_view.without_ui(cache_timeout=0)),
        name='schema-json'
    ),
    url(
        r'^swagger/$',
        login_required(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui'
    ),
    url(
        r'^redoc/$',
        login_required(schema_view.with_ui('redoc', cache_timeout=0)),
        name='schema-redoc'
    ),

    path('login/', LoginView.as_view(), name='login'),
    path('logout', logout_request, name='logout'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('api/blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
