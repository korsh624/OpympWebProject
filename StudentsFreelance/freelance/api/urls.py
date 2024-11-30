from django.urls import path

from .views import AddCommentsView, AddOrderView


urlpatterns = [
    path('add-comment/', AddCommentsView.as_view()),
    path('add-order/', AddOrderView.as_view())
]