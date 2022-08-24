from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<str:detail>', views.details, name='details'),
    path('data/', views.getdata, name='data'),
]
