from django.contrib import admin
from imobiliaria.models import Imovel

class ListarImoveis(admin.ModelAdmin):
    list_display = ('id','endereco', 'bairro', 'categoria','publicada')
    list_display_links = ('endereco',)
    search_fields = ('endereco',)
    list_editable = ('publicada',)
    

admin.site.register(Imovel, ListarImoveis)
