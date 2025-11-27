from pyexpat.errors import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from imobiliaria.models import Imovel
from imobiliaria.forms import ImovelForms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

@csrf_exempt
def cadastrar(request): # 
    # 1. Se for POST (clicou no botão enviar)
    if request.method == 'POST':
        form = ImovelForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('home') # Retorno 1: Redireciona se deu certo
            
    # 2. Se for GET (apenas abriu a página)
    else:
        form = ImovelForms()

    return render(request, 'cadastrar.html', {'form': form})

def home(request):
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True)

    # --- ADICIONE ESTA LINHA AQUI TAMBÉM ---
    lista_bairros = Imovel.objects.values_list('bairro', flat=True).distinct().order_by('bairro')

    # Não esqueça de passar "bairros": lista_bairros no dicionário final
    return render(request, "home.html", {"cards": imoveis, "bairros": lista_bairros})


def imagem(request, foto_id):
    imovel = get_object_or_404(Imovel, pk=foto_id)
    return render(request, 'imagem.html', {"imovel": imovel})


def buscar(request):
    # 1. Começa trazendo todos
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True)

    lista_bairros = Imovel.objects.values_list('bairro', flat=True).distinct().order_by('bairro')

    # 2. Captura os dados vindos do HTML
    # O nome dentro do get('...') DEVE ser igual ao name="..." do HTML
    tipo_filtrar = request.GET.get('categoria') 
    bairro_filtrar = request.GET.get('bairro')
    tamanho_filtrar = request.GET.get('tamanho')
    valor_min_filtrar = request.GET.get('valor_min') # Corrigido
    valor_max_filtrar = request.GET.get('valor_max') # Corrigido

    # 3. Aplica os filtros

    if tipo_filtrar:
        # iexact: ignora maiúsculas. Busca 'casa', 'Casa' ou 'CASA'
        # Verifique se no seu banco o campo chama 'categoria' ou 'tipo'
        # Aqui estou assumindo que no banco chama 'categoria'. Se for 'tipo', mude para imoveis.filter(tipo__iexact=...)
        imoveis = imoveis.filter(categoria__iexact=tipo_filtrar)

    if bairro_filtrar:
        imoveis = imoveis.filter(bairro__iexact=bairro_filtrar)

    if tamanho_filtrar:
        imoveis = imoveis.filter(tamanho__gte=tamanho_filtrar)

    if valor_min_filtrar:
        imoveis = imoveis.filter(valor__gte=valor_min_filtrar)

    if valor_max_filtrar:
        imoveis = imoveis.filter(valor__lte=valor_max_filtrar)

    return render(request, "home.html", {"cards": imoveis, "bairros": lista_bairros})


def filtro(request, categoria):
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True, categoria=categoria)
    return render(request,'index.html',{"cards": imoveis})


# 1. Crie uma função simples de checagem
def eh_superuser(user):
    return user.is_superuser

# 2. Aplique o decorador na sua view de cadastro
@user_passes_test(eh_superuser, login_url='/admin/login/?next=/') 
def cadastrar_imagem(request):
    # O código da sua função continua aqui...
    # Se o usuário NÃO for superuser, o Django nem deixa chegar aqui.
    return render(request, 'galeria/cadastrar_imagem.html')


