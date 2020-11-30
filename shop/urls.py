from pprint import pprint

from django.urls import path
from rest_framework import routers

from shop.views import PartnerUpdate, InitData, \
    ProductInfoView, SingleProductInfoView, PartnerOrders, OrderViewSet, BasketListView, BasketViewSet

# , BasketView

app_name = 'shop'

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet)
router.register(r'basket', BasketViewSet, basename="basket")

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('initdata/', InitData.as_view(), name='init-data'),
    path('products/', ProductInfoView.as_view(), name='shops'),
    path('singleproduct/', SingleProductInfoView.as_view(), name='prod'),
    # path('basket/', BasketView.as_view(), name='basket'),
    path('basketlist/', BasketListView.as_view(), name='basket-list-apiview'),

    path('partner/orders/', PartnerOrders.as_view(), name='partner-orders'),

]
urlpatterns += router.urls
pprint(urlpatterns)
