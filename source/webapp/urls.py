from django.urls import path

from webapp.views import IndexView, CreateProduct, ProductView, DeleteProduct, UpdateProduct
from webapp.views.review import CreateReviewView

app_name = "webapp"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('product/add/', CreateProduct.as_view(), name="create_product"),
    path('product/<int:pk>/', ProductView.as_view(), name="product_view"),
    path('product/<int:pk>/delete/', DeleteProduct.as_view(), name="delete_product"),
    path('product/<int:pk>/update/', UpdateProduct.as_view(), name="update_product"),
    path('product/<int:pk>/review/add/', CreateReviewView.as_view(), name="product_review_create"),

]
