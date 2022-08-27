from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from webapp.forms import ReviewForm
from webapp.models import Product


class CreateReviewView(CreateView):
    form_class = ReviewForm
    template_name = "reviews/create.html"

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        user = self.request.user
        form.instance.product = product
        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})