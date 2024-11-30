from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    path('', views.index_page, name='home'),
    path('search/', views.search_page, name='search'),
    path('order/<int:order_id>', views.detail_page, name='detail')
]