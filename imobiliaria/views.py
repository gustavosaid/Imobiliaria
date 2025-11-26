from pyexpat.errors import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q  # <--- IMPORTANTE: Importe o Q
from imobiliaria.models import Imovel
from imobiliaria.forms import ImovelForms
from django.views.decorators.csrf import csrf_exempt


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
    return render(request, 'visualizar.html', {"cards": imoveis})


def imagem(request, foto_id):
    imovel = get_object_or_404(Imovel, pk=foto_id)
    return render(request, 'imagem.html', {"imovel": imovel})


def buscar(request):
# Começa trazendo todos
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True)

    # 1. Filtro por Texto Geral (barra de busca do topo, se houver)
    if "buscar" in request.GET:
        nome_a_buscar = request.GET.get('buscar')
        
        if nome_a_buscar:
            # O "Q" permite usar o operador "OU" (|)
            # Aqui estamos dizendo: Traga se o texto estiver na descrição OU no título OU na categoria
            imoveis = imoveis.filter(
                Q(categoria__icontains=nome_a_buscar) # Verifique se o nome do campo no seu Model é 'categoria' ou 'tipo'
            )


    return render(request, "visualizar.html", {"cards": imoveis})


def filtro(request, categoria):
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True, categoria=categoria)
    return render(request,'index.html',{"cards": imoveis})

