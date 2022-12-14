from django import forms

from webapp.models import Product, Review


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "image"]


class UserProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text", "mark"]

