from django.urls import path
from store import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


app_name = 'store'

urlpatterns = [

    path('favicon\.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),

    path('update_item/',views.updateUserOrder,name='update_item'),
    path('cart/update_item/',views.updateUserOrder,name='cart_update_item'),

    path('process_order/',views.processOrder,name='process_order'),

    path('signup/',views.SignUp.as_view(),name='signup'),
    path('store/login/',auth_views.LoginView.as_view(
    template_name = 'store/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),

    path('<int:pk>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('my_orders/<int:pk>/',views.myOrder,name='myorders'),

    path('player/<str:name>',views.playerProduct,name='player'),
    path('player/update_item/',views.updateUserOrder,name='cart_update_item'),

]
