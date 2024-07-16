from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def list_products(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, template_name='product_list.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, template_name='product_detail.html', context=context)

