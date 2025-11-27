from django.db import models

class Imovel(models.Model):
    TIPO_IMOVEL = [
        ("APARTAMENTO",'Apartamento'),
        ("CASA","Casa"),
        ("PONTO COMERCIAL", "Ponto Comercial")
    ]
    categoria = models.CharField(max_length=100, choices=TIPO_IMOVEL, default='')
    tamanho = models.IntegerField()
    numero_quarto = models.IntegerField(default=1)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    bairro = models.CharField(max_length=50, blank=False)
    endereco = models.CharField(max_length=50, blank=False)
    numero = models.CharField(max_length=5, blank=False)
    descricao = models.CharField(max_length=250,null=False, blank=False)
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    publicada = models.BooleanField(default=True)

class ImagemImovel(models.Model):
    imovel = models.ForeignKey(Imovel, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="fotos_extras/%Y/%m/%d/")

    def __str__(self):
        return f"Imagem de {self.imovel}"
