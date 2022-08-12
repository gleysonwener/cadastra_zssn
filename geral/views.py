from .serializers import ItemSerializer, SobreviventeSerializer, InventarioSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Item, Sobrevivente, Inventario
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response



# listar e cadastrar itens
class ItemListCreateAPIView(ListCreateAPIView):
    
    serializer_class = ItemSerializer
    queryset = Item.objects.all()



#listar e cadastrar os sobreviventes
class SobreviventeListCreateAPIView(ListCreateAPIView):
    
    serializer_class = SobreviventeSerializer
    queryset = Sobrevivente.objects.all()



#listar e cadastrar o inventario de cada sobrevivente
class InventarioListCreateAPIView(ListCreateAPIView):
    
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()



# atualizando as informações do sobrevivente
class SobreviventeLocalUpdate(APIView):
    

    def patch(self, request, sobrevivente_id):

        sobrevivente = get_object_or_404(Sobrevivente, pk=sobrevivente_id)
        serializer = SobreviventeSerializer(Sobrevivente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Não foi possível fazer a atualização'})



# troca de itens do sobrevivente
@api_view(['POST'])
def troca_itens(request):
    
    try:

        sobrevivente1 = Sobrevivente.objects.get(id=request.data.get('sobrevivente1'), infectado=False)
        sobrevivente2 = Sobrevivente.objects.get(id=request.data.get('sobrevivente2'), infectado=False)
        sobrevivente1_item = Item.objects.get(id=request.data.get('sobrevivente1_item'))
        sobrevivente2_item = Item.objects.get(id=request.data.get('sobrevivente2_item'))
        inventario_sobrevivente1 = Inventario.objects.get(sobrevivente=sobrevivente1, item=sobrevivente1_item)
        inventario_sobrevivente2 = Inventario.objects.get(sobrevivente=sobrevivente1, item=sobrevivente2_item)

    except Sobrevivente.DoesNotExist:
        return Response({'message': 'Nenhum sobreviventeencontrado ou está infectado'})

    except Item.DoesNotExist:
        return Response({'message': 'Item não existe'})
    
    except Inventario.DoesNotExist:
        return Response({'message': 'Sobrevivente não tem o item no inventário'})

    sobrevivente1_item_quantidade = request.data.get('sobrevivente1_item_quantidade')
    sobrevivente2_item_quantidade = request.data.get('sobrevivente2_item_quantidade')

    if sobrevivente1 != sobrevivente2:

        pontos_quantidade_sobrevivente1 = item_sobrevivente1.pontos * item_sobrevivente1_quantidade
        pontos_quantidade_sobrevivente2 = item_sobrevivente2.pontos * item_sobrevivente2_quantidade
       
        if pontos_quantidade_sobrevivente1 == pontos_quantidade_sobrevivente2:
            
            inventario_sobrevivente1.quantidade -= item_sobrevivente1_quantidade
            inventario_sobrevivente2.quantidade -= item_sobrevivente2_quantidade

            adciona_item_sobrevivente1 = Inventario.objects.get(sobrevivente=sobrevivente1, item=item_sobrevivente2)
            adciona_item_sobrevivente1.quantidade += item_sobrevivente2_quantidade

            adciona_item_sobrevivente1.save()
            
            adciona_item_sobrevivente2 = Inventario.objects.get(sobrevivente=sobrevivente2, item=item_sobrevivente1)
            adciona_item_sobrevivente1.quantidade += item_sobrevivente2_quantidade

            adciona_item_sobrevivente1.save()

           
            if inventario_sobrevivente1.quantidade < 0:
                inventario_sobrevivente1.quantidade = 0
                inventario_sobrevivente1.save()
            
            else:
                inventario_sobrevivente1.save()
            
            if inventario_sobrevivente2.quantidade < 0:
                inventario_sobrevivente2.quantidade = 0
                inventario_sobrevivente2.save()
            
            else:
                inventario_sobrevivente2.save()
            return Response({'message': 'Troca realizada com sucesso'})

        return Response({'message': 'Não foi possível efetuar a troca'})
    
    return Response({'message': 'Você nao pode trocar item com você'})



@api_view(['POST'])
def marca_infectado(request):
    try:
        sobrevivente1 = Sobrevivente.objects.get(id=request.data.get('sobrevivente'), infectado=False)
        sobrevivente2 = Sobrevivente.objects.get(id=request.data.get('sobrevivente2'), infectado=False)
        sobrevivente3 = Sobrevivente.objects.get(id=request.data.get('sobrevivente3'), infectado=False)
        
        sobrevivente_infectado = Sobrevivente.objects.get(id=request.data.get('sobrevivente_infectado'))

    except Sobrevivente.DoesNotExist:

        return Response({'message': 'Veja se ossobreviventes foram cadastrados no sistema e não estao infectados'})

        
    lista_sobreviventes = set([sobrevivente1, sobrevivente2, sobrevivente3])
    
    if len(lista_sobreviventes) >= 3 and sobrevivente_infectado not in lista_sobreviventes:

        if sobrevivente_infectado.infectado:

            return Response({'message': 'marcado como infectado'})
        
        else:

            sobrevivente_infectado.infectado = True
            sobrevivente_infectado.save()
        
        return Response({'message': 'Sobrevivente foi marcado como infectado'})

    return Response({'message': 'Não foi possível realizar a operação. É necessário três sobreviventes únicos e o suspeito de estar infectado não pode ser quem acusa'})


# relatórios
# percentual infectados 
@api_view(['GET'])
def rel_porcentagem_infectados(request):

    sobreviventes = Sobrevivente.objects.all()
    sobrevivente_infectado = sobreviventes.filter(infectado=True)
    percentual_infectados = sobrevivente_infectado.count() / sobreviventes.count() * 100

    return Response({'Porcentagem de Sobreviventes Infectados': '{0:.2f}'.format(percentual_infectados)})


#percentual não infectados
@api_view(['GET'])
def rel_porcentagem_nao_infectados(request):
    
    sobreviventes = Sobrevivente.objects.all()
    sobrevivente_nao_infectado = sobreviventes.filter(infectado=False)
    percentual_nao_infectados = sobrevivente_nao_infectado.count() / sobreviventes.count() * 100
 
    return Response({'Porcentagem de Sobreviventes Infectados': '{0:.2f}'.format(percentual_nao_infectados)})


# média de itens / sobreviventes
@api_view(['GET'])
def rel_media_itens_sobreviventes(request):
    
    sobreviventes = Sobrevivente.objects.count()
    inventario = Inventario.objects.values('item__nome').order_by('item').annotate(total_itens=Sum('quantidade'))
    
    print('inventario.all', inventario.all())

    rel_data = []

    for invent in inventario:
        
        rel_data.append(
            {
                'item': invent.get('item__nome'),
                'media_de_sobreviventes': '{0:.2f}'.format(invent.get('total_itens') / sobreviventes)
            }
        )

    return Response(rel_data)



# quantidade de pontos perdidos
@api_view(['GET'])
def rel_pontos_perdidos(request):
    
    sobreviventes_infectados = Sobrevivente.objects.filter(infectado=True)
    lista_soreviventes_infectados = []
    total_pontos_perdidos = 0

    for sob in sobreviventes_infectados:
    
        lista_soreviventes_infectados.append(sob.nome)
        inventario = Inventario.objects.filter(sobrevivente=sob)
    
        for invent in inventario:
            total_pontos_perdidos += sob.item.pontos
    
    rel_data = {
        'total_pontos_perdidos': total_pontos_perdidos,
        'lista_soreviventes_infectados': lista_soreviventes_infectados
    }
    
    return Response(rel_data)