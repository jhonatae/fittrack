from django.contrib import admin
from django.urls import include, path
from treinos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('treinos.urls')),
    path('fichas/editar/<int:pk>/', views.editar_ficha, name='editar_ficha'),
]
