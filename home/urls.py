from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path("nova/", views.nova_mensagem, name="nova_mensagem"),   # ← novo
]
