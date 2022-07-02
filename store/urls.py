from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout'),
    path('update_item/', views.updateItem, name='update-item')

]
