from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, StyleFormMixin, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
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
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_products')

    def get_form_class(self):
        form_class = super().get_form_class()
        return type(form_class.__name__, (form_class, StyleFormMixin), {})


class ProductUpdateView(UpdateView):
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
