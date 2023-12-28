from django.urls import path

from . import views


app_name = 'product'

urlpatterns = [
    path('', views.products, name='products'),
    path('woman', views.woman, name='woman'),
    path('products/woman/', views.woman, name='woman'),
    path('products/woman/', views.man, name='man'),

    path('man', views.man, name='man'),    
    path('<int:pk>/', views.details, name='details'),
    path('search_results/', views.search_results, name='search_results'),  # Use search_results view


]