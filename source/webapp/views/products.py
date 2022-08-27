from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from webapp.forms import SearchForm, ProductForm, UserProductForm
from webapp.models import Product
from django.utils.http import urlencode


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    ordering = "name"
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Product.objects.filter(Q(name__icontains=self.search_value))
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class CreateProduct(PermissionRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = "products/create_product.html"
    permission_required = "webapp.add_product"



    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.pk})


class ProductView(LoginRequiredMixin, DetailView):
    template_name = "products/product_view.html"
    model = Product
    context_object_name = "product"



class DeleteProduct(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = "webapp.delete_product"

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:index")


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    form_class = ProductForm
    template_name = "products/product_update.html"
    model = Product
    permission_required = "webapp.change_product"


    def get_form_class(self):
        if self.request.GET.get("is_admin"):
            return ProductForm
        return UserProductForm

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.pk})