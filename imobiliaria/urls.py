from django.urls import path
from imobiliaria.views import cadastrar, home, imagem, filtro, buscar, deletar_imovel, editar_imovel
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial de login
    path('', home, name='home'),  
    path('cadastrar', cadastrar, name='cadastrar_imagem'),
    path('imagem/<int:foto_id>', imagem, name='imagem'),
    path('buscar', buscar, name='buscar'),
    path('filtro/<str:categoria>', filtro, name='filtro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar/<int:id>/', editar_imovel, name='editar_imovel'),
    path('deletar/<int:id>/', deletar_imovel, name='deletar_imovel'),
]