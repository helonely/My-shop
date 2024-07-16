from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import list_products, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('', list_products, name='list_products'),
    path('products/<int:pk>/', product_detail, name='product_detail'),

]
