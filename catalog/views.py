from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:list_products')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:list_products')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:list_products')


class ContactsView(View):
    template_name = 'products/contacts.html'

    def get(self, request, *args, **kwargs):
        # GET-запрос
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        print(name, message, phone)
        # возвращаем пользователю ту же страницу с формой
        return render(request, self.template_name)
