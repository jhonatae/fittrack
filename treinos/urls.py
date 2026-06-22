from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('exercicios/novo/', views.cadastrar_exercicio, name='cadastrar_exercicio'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('cadastro/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path("editar/<int:pk>/", views.editar_exercicio, name="editar_exercicio"),
    path("deletar/<int:pk>/", views.deletar_exercicio, name="deletar_exercicio"),
]