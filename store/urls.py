from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('objednavka/', views.order_submit, name='order_submit'),
    path('potvrzeni/', views.order_success, name='order_success'),
    path('potvrzeni/<int:objednavka_id>/', views.order_success, name='order_success'),

]