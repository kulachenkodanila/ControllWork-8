from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.forms import ReviewForm
from webapp.models import Product, Review


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


class UpdateReview(UserPassesTestMixin, UpdateView):
    form_class = ReviewForm
    template_name = "reviews/update.html"
    model = Review

    def test_func(self):
        return self.get_object().author == self.request.user or\
               self.request.user.has_perm('webapp.change_review')

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})



class DeleteReview(DeleteView):
    model = Review

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.object.product.pk})