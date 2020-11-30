from pprint import pprint

from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from shop_user.views import Account, CustomObtainAuthToken, ContactViewSet

app_name = "shop_user"

router = routers.SimpleRouter()
router.register(r'account', Account)
router.register(r'contact', ContactViewSet, basename='contact')

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('account/get-token/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
]

urlpatterns += router.urls

pprint(urlpatterns)
