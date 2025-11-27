from django.contrib import admin
from imobiliaria.models import Imovel,ImagemImovel

class ImagemImovelInline(admin.TabularInline):
    model = ImagemImovel
    extra = 1

# 2. Modifique a sua classe JÁ EXISTENTE (ListarImoveis)
class ListarImoveis(admin.ModelAdmin):
    # Mantenha suas configurações antigas aqui (list_display, search_fields, etc)
    list_display = ('id', 'valor', 'numero_quarto', 'tamanho', 'categoria')
    list_display_links = ('id', 'valor')
    search_fields = ('valor',)
    list_editable = ('categoria',)
    list_per_page = 10

    # ADICIONE APENAS ESTA LINHA:
    inlines = [ImagemImovelInline]

# 3. Mantenha apenas UM registro
admin.site.register(Imovel, ListarImoveis)

# Não precisa registrar a ImagemImovel separadamente, ela já aparece dentro do Imovel
# admin.site.register(ImagemImovel)
