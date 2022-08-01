"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from myapp import views

"""
Swagger
"""

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="MoWa API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'user', views.UserListViewSet)
router.register(r'activity', views.ActivityListViewSet)

urlpatterns = [
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('myapp.urls')),

    path('admin/', admin.site.urls),

    path('user/all', views.UserListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('activity/all', views.ActivityListViewSet.as_view({'get': 'list', 'post': 'create'})),

]
