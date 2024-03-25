from django.urls import path

from .views import products_view, product_view_detail, category_list_view


app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_view_detail, name='product_detail'),
    path('search/<slug:slug>/', category_list_view, name='category_list'),
]
