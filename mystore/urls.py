from django.urls import path

from .views import *
from . import views
from .api import *

app_name = 'mystore'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add_item/', views.add_item, name="add_item"),
    path('product/<slug>/edit_item/', views.edit_item, name='edit_item'),
    path('product/<slug>/delete/', views.delete_item, name='delete_item'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('api/v1/items', ListItem.as_view(), name='items'),
    path('api/v1/items/<int:pk>/', DetailItem.as_view(), name='item'),
    path('<str:room_name>/', views.room, name='room'),
]
