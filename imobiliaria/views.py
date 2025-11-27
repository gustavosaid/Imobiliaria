from pyexpat.errors import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from imobiliaria.models import Imovel, ImagemImovel
from imobiliaria.forms import ImovelForms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

@csrf_exempt
def cadastrar(request):
    # 1. SEGURANÇA: Checa quem está tentando entrar
    
    # Se NÃO estiver logado -> Manda para o login do Admin e depois volta pra cá
    if not request.user.is_authenticated:
        return redirect(f'/admin/login/?next={request.path}')

    # Se estiver logado, mas NÃO for Admin -> Chuta para a home com erro
    if not request.user.is_superuser:
        messages.error(request, "Acesso negado: Apenas administradores podem cadastrar.")
        return redirect('home') # Confirme se o nome da sua url inicial é 'home' ou 'index'

    # 2. LÓGICA DO FORMULÁRIO
    if request.method == 'POST':
        form = ImovelForms(request.POST, request.FILES)
        
        # Pega a lista de arquivos do input 'multiple'
        imagens_extras = request.FILES.getlist('imagens_extras')

        if form.is_valid():
            # Salva o imóvel (Capa e dados) e guarda na variável 'imovel_criado'
            imovel_criado = form.save()

            # Loop para salvar cada foto extra vinculada a este imóvel
            for arquivo in imagens_extras:
                ImagemImovel.objects.create(imovel=imovel_criado, imagem=arquivo)

            # messages.success(request, "Imóvel e fotos cadastrados com sucesso!")
            return redirect('home')
            
    else:
        form = ImovelForms()

    return render(request, 'cadastrar.html', {'form': form})

def home(request):
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True)
    varias_imagens = Imovel.objects.order_by("valor").filter(publicada=True).prefetch_related('imagens')

    # --- ADICIONE ESTA LINHA AQUI TAMBÉM ---
    lista_bairros = Imovel.objects.values_list('bairro', flat=True).distinct().order_by('bairro')
    tamanho_busca = request.GET.get('tamanho')

    if tamanho_busca:
        imoveis = imoveis.filter(tamanho__lte=tamanho_busca)

    # Não esqueça de passar "bairros": lista_bairros no dicionário final
    return render(request, "home.html", {"cards": imoveis, "bairros": lista_bairros, "varias_imagens": varias_imagens})


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
    valor_min_filtrar = request.GET.get('valor_min') 
    valor_max_filtrar = request.GET.get('valor_max') 

    # 3. Aplica os filtros
    if tipo_filtrar:
        imoveis = imoveis.filter(categoria__iexact=tipo_filtrar)

    if bairro_filtrar:
        imoveis = imoveis.filter(bairro__iexact=bairro_filtrar)

    if tamanho_filtrar:
        imoveis = imoveis.filter(tamanho__lte=tamanho_filtrar)

    if valor_min_filtrar:
        imoveis = imoveis.filter(valor__gte=valor_min_filtrar)

    if valor_max_filtrar:
        imoveis = imoveis.filter(valor__lte=valor_max_filtrar)

    return render(request, "home.html", {"cards": imoveis, "bairros": lista_bairros})


def filtro(request, categoria):
    imoveis = Imovel.objects.order_by("valor").filter(publicada=True, categoria=categoria)
    return render(request,'index.html',{"cards": imoveis})

@csrf_exempt
def eh_superuser(user):
    return user.is_superuser

@csrf_exempt
# 2. Aplique o decorador na sua view de cadastro
@user_passes_test(eh_superuser, login_url='/admin/login/?next=/') 
def cadastrar_imagem(request):
    
    return render(request, 'galeria/cadastrar_imagem.html')

@csrf_exempt
def editar_imovel(request, id):
    # Pega o imóvel ou dá erro 404 se não existir
    imovel = get_object_or_404(Imovel, id=id)

    # Segurança: Só admin entra
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        # Preenche o form com os dados novos + a instância antiga (para atualizar, não criar novo)
        form = ImovelForms(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        # Preenche o form com os dados atuais do banco
        form = ImovelForms(instance=imovel)

    return render(request, 'cadastrar.html', {'form': form}) # Reusa o template de cadastro

@csrf_exempt
# View de Deletar
def deletar_imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)

    # Segurança
    if not request.user.is_superuser:
        return redirect('home')

    # Deleta direto
    imovel.delete()
    return redirect('home')


