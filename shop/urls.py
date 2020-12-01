from pprint import pprint

from django.urls import path
from rest_framework import routers

from shop.views import PartnerUpdate, InitData, \
    ProductInfoView, SingleProductInfoView, PartnerOrders, OrderBuyerViewSet, BasketListView, BasketViewSet

app_name = 'shop'

router = routers.SimpleRouter()
router.register(r'orderbuyer', OrderBuyerViewSet, basename="orderbuyer")
router.register(r'basket', BasketViewSet, basename="basket")

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('initdata/', InitData.as_view(), name='init-data'),
    path('products/', ProductInfoView.as_view(), name='shops'),
    path('singleproduct/', SingleProductInfoView.as_view(), name='prod'),
    path('basketlist/', BasketListView.as_view(), name='basket-list-apiview'),

    path('partner/orders/', PartnerOrders.as_view(), name='partner-orders'),

]
urlpatterns += router.urls
pprint(urlpatterns)
