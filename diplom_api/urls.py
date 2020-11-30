from pprint import pprint
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from shop.views import CeleryTaskView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/', CeleryTaskView.as_view(), name='task'),
    url(r'^user/', include('shop_user.urls', namespace='user')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    path('openapi/', get_schema_view(
        title="DiplomAPI (shop)",
        description="API for shop",
        version="1.2.0",
        permission_classes=(permissions.AllowAny,),
        # url='http://localhost:8000/',    # better not have this because Postman add {{baseUrl}} by default anyway.
        public=True,
    ), name='openapi-schema')]
pprint(urlpatterns)
