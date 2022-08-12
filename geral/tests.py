from . models import Sobrevivente, Inventario, Item 
from django.test import TestCase





class InventarioTestCase(TestCase):

    def setUp(self):
        sobrevivente = Sobrevivente.objects.create(
            nome="gleyson",
            idade=40,
            sexo="M",
            longitude=824578,
            latitude=784512
        )
        item = Item.objects.create(name='água', points=4)
        Inventario.objects.create(sobrevivente=sobrevivente, item=item, quantidade=3)

    def retorno_teste(self):
        inventario = Inventario.objects.get(id=1)
        self.assertEquals(inventario.__str__(), "gleyson")


class SobreviventeTestCase(TestCase):

    def setUp(self):
        Sobrevivente.objects.create(
            nome="gleyson",
            idade=40,
            sexo="M",
            longitude=824578,
            latitude=784512
        )

    def retorno_teste(self):
        sobrevivente = Sobrevivente.objects.get(name="gleyson")
        self.assertEquals(sobrevivente.__str__(), "gleyson")


class ItemTestCase(TestCase):

    def setUp(self):
        Item.objects.create(nome='água', pontos=4)
        Item.objects.create(nome='alimentação', pontos=3)

    def retorno_teste(self):
        item1 = Item.objects.get(nome='água')
        item2 = Item.objects.get(nome='alimentação')
        self.assertEquals(item1.__str__(), "água")
        self.assertEquals(item2.__str__(), "alimentação")