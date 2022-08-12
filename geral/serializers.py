from . model import Sobrevivente, Item, Inventario
from rest_framework import serializers



class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class SobreviventeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sobrevivente
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventario
        fields = '__all__'