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
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.schemas.openapi import SchemaGenerator


from shop.views import PartnerUpdate, RegisterAccount, ConfirmAccount, AccountDetails, LoginAccount, InitData, \
    ProductInfoView, SingleProductInfoView, BasketView, PartnerOrders, CeleryTaskView, AccountViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r'account', AccountViewSet)
router.register(r'order', OrderViewSet, basename="order",)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details', AccountDetails.as_view(), name='user-details'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('initdata', InitData.as_view(), name='init-data'),
    path('products', ProductInfoView.as_view(), name='shops'),
    path('singleproduct', SingleProductInfoView.as_view(), name='prod'),
    path('basket', BasketView.as_view(), name='basket'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    path('task/', CeleryTaskView.as_view(), name='task'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('partner/state', PartnerState.as_view(), name='partner-state'),
    # path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    # path('user/contact', ContactView.as_view(), name='user-contact'),
    # path('user/password_reset', reset_password_request_token, name='password-reset'),
    # path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    # path('categories', CategoryView.as_view(), name='categories'),
    # path('shops', ShopView.as_view(), name='shops'),
    #
    #
    # path('order', OrderView.as_view(), name='order'),
]
urlpatterns += router.urls
urlpatterns += [path('openapi/', get_schema_view(
        title="DiplomAPI (shop)",
        description="API for shop",
        version="1.0.1",
        # url='http://127.0.0.1:8000/'
    ), name='openapi-schema')]
# pprint(urlpatterns)

# generator = SchemaGenerator(title='Stock Prices API')
# schema = generator.get_schema()
# print(schema)
