from django.urls import path
from imobiliaria.views import cadastrar, home, imagem, filtro, buscar

urlpatterns = [
    # Página inicial de login
    path('', home, name='home'),  
    path('cadastrar', cadastrar, name='cadastrar_imagem'),
    path('imagem/<int:foto_id>', imagem, name='imagem'),
    path('buscar', buscar, name='buscar'),
    path('filtro/<str:categoria>', filtro, name='filtro'),
]