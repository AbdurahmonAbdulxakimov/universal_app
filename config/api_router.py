from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from users.api.views import UserViewSet
from shop import views as shop_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path(
        "shop/cart/",
        shop_views.CartListCreateAPIView.as_view(),
        name="cart-list-create",
    ),
    path(
        "shop/cart/<int:pk>/",
        shop_views.CartDestroyAPIView.as_view(),
        name="cart-destroy",
    ),
    path(
        "shop/checkout/",
        shop_views.CheckoutListCreateAPIView.as_view(),
        name="checkout",
    ),
]
urlpatterns += router.urls
