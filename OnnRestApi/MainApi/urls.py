from django.conf.urls import url
from MainApi import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r"^products$", views.product_list, name="products"),
    url(r"^products/(?P<pk>[0-9]+)$", views.product_detail, name="delete-product"),
    url(r"^orders$", views.order_list, name="orders"),
    url(r"^token$", obtain_auth_token, name="obtain-token"),
]
