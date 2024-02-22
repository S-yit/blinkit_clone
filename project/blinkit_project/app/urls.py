from django.urls import path
from . import views

urlpatterns = [
    path('product_list',views.product_list,name="product_list"),
    path('<int:id>',views.product_details,name='product_details'),
    path('',views.signup),
    path('login_view',views.login_view),
    path('logout_view',views.logout_view),
    path('search_result',views.search_result,name='search_result'),
    path('add_to_cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('cart-items',views.cart_items,name='cart_items'),
    path('remove_from_cart/<int:product_id>',views.remove_from_cart,name='remove_from_cart'),
    path('add_address',views.add_address,name='add_address'),
    #path('set_delivery_address',views.set_delivery_address,name='set_delivery_address'),
    path('order_review/<int:sa_id>',views.order_review,name='order_review'),
    path('checkout_order/<int:sa_id>',views.checkout_order,name='checkout_order'),
    path('payment-order/', views.payment_order, name="payment_order"),
    path('payment-process/<int:order_id>/<int:amount>', views.payment_process, name="payment_process")
]
