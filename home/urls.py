from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path("nova/", views.nova_mensagem, name="nova_mensagem"),   # ← novo
    path("mensagens/<int:id>/editar/", views.editar_mensagem, name="editar_mensagem"),   # ← novo
    path("mensagens/<int:id>/remover/", views.remover_mensagem, name="remover_mensagem"),  # ← novo
]
