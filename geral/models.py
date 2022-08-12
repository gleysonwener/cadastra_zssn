from django.db import models



class Item(models.Model):
    nome = models.CharField('Item', max_length=150)
    pontos = models.PositiveIntegerField('Pontos')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        ordering = ['id']

    def __str__(self):
        return self.nome


class Sobrevivente(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    nome = models.CharField('Nome', max_length=200)
    idade = models.PositiveIntegerField('Idade')
    sexo = models.CharField('Sexo', max_length=1, choices=SEXO)
    longitude = models.FloatField('Longitude')
    latitude = models.FloatField('Latitude')
    infectado = models.BooleanField('Infectado?', default=False)

    class Meta:
        verbose_name = 'Sobrevivente'
        verbose_name_plural = 'Sobreviventes'
        ordering = ['id']

    def __str__(self):
        return self.nome


class Inventario(models.Model):

    sobrevivente = models.ForeignKey(Sobrevivente, verbose_name='Sobrevivente', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name='Item', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField('Quantidade')

    class Meta:
        verbose_name = 'Inventário'
        verbose_name_plural = 'Inventários'
        ordering = ['id']

    def __str__(self):
        return self.sobrevivente.nome