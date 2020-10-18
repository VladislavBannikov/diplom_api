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

from django.contrib import admin
from django.urls import path
from rest_framework import routers

from shop.views import PartnerUpdate, RegisterAccount, ConfirmAccount, AccountDetails, LoginAccount, InitData, \
    ProductInfoView, SingleProductInfoView, BasketView, OrderView, PartnerOrders, CeleryTaskView, AccountViewSet

router = routers.SimpleRouter()
router.register(r'account', AccountViewSet)

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
    path('order', OrderView.as_view(), name='order'),
    path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),

    path('task/', CeleryTaskView.as_view(), name='task'),

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

