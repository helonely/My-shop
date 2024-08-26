from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, StyleFormMixin, VersionForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_categories_from_cache, get_products_from_cache


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    extra_context = {
        'title': "Категории"
    }

    def get_queryset(self):
        return get_categories_from_cache()


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение текущих версий для каждого продукта
        products_with_versions = []
        for product in self.get_queryset():
            current_version = Version.objects.filter(product=product, is_active=False).first()
            products_with_versions.append((product, current_version))

        context['products_with_versions'] = products_with_versions

        return context

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_products')

    def get_form_class(self):
        form_class = super().get_form_class()
        return type(form_class.__name__, (form_class, StyleFormMixin), {})

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_products')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_publish_post') and user.has_perm('catalog.can_edit_description'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
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
