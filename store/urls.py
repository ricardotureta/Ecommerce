from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
 	path('sair', views.sair, name='sair'),
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('login/', views.login, name="login"),
 	path('cadastro/', views.usuario_cadastro, name="usuario_cadastro"),
]