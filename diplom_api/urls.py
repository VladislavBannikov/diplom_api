"""diplom_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from pprint import pprint
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view
from shop.views import PartnerUpdate, InitData, \
    ProductInfoView, SingleProductInfoView, BasketView, PartnerOrders, CeleryTaskView, OrderViewSet, Account, \
    CustomObtainAuthToken

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet, basename="order",)
router.register(r'account', Account)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('initdata', InitData.as_view(), name='init-data'),
    path('products', ProductInfoView.as_view(), name='shops'),
    path('singleproduct', SingleProductInfoView.as_view(), name='prod'),
    path('basket', BasketView.as_view(), name='basket'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('task/', CeleryTaskView.as_view(), name='task'),
    path('account/get-token/', CustomObtainAuthToken.as_view(), name='api_token_auth'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += router.urls
urlpatterns += [path('openapi/', get_schema_view(
        title="DiplomAPI (shop)",
        description="API for shop",
        version="1.1.0",
        permission_classes=(permissions.AllowAny,),
        # url='http://localhost:8000/',    # better not have this because Postman add {{baseUrl}} by default anyway.
        public=True,
    ), name='openapi-schema')]
pprint(urlpatterns)
