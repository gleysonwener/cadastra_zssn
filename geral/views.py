from .serializers import ItemSerializer, SobreviventeSerializer, InventarioSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from .models import Item, Survivor, Inventory
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class ItemListCreateAPIView(ListCreateAPIView):
    # listar e cadastrar itens
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAdminUser]


class SobreviventeListCreateAPIView(ListCreateAPIView):
    #listar e cadastrar os sobreviventes
    serializer_class = SobreviventeSerializer
    queryset = Sobrevivente.objects.all()


class InventarioListCreateAPIView(ListCreateAPIView):
    #listar e cadastrar o inventario de cada sobrevivente
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()
    permission_classes = [IsAdminUser]


class SobreviventeLocalUpdate(APIView):
    
    # atualizando as informações do sobrevivente
    def patch(self, request, sobrevivente_id):
        sobrevivente = get_object_or_404(Sobrevivente, pk=sobrevivente_id)
        serializer = SobreviventeSerializer(Sobrevivente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Não foi possível fazer a atualização'})


@api_view(['POST'])
def troca_itens(request):
    # troca de itens do sobrevivente
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
    
    return Response({'message': "Você nao pode trocar item com você mesmo})


@api_view(['POST'])
def mark_survivor_as_infected(request):
    """
    Marca um sobrevivente como infectado. É necessário fornecer a informação de 3 sobreviventes que confirmam a infecção e a informação do
    infectado.
    """
    try:
        survivor1 = Survivor.objects.get(id=request.data.get('survivor1'), infected=False)
        survivor2 = Survivor.objects.get(id=request.data.get('survivor2'), infected=False)
        survivor3 = Survivor.objects.get(id=request.data.get('survivor3'), infected=False)
        survivor_infected = Survivor.objects.get(id=request.data.get('survivor_infected'))
    except Survivor.DoesNotExist:
        return Response({'message': _('Confirme se todos os sobreviventes estão cadastrados no sistema e que não estão infectados.')})
    survivor_list = set([survivor1, survivor2, survivor3])
    if len(survivor_list) >= 3 and survivor_infected not in survivor_list:
        if survivor_infected.infected:
            return Response({'message': _('Sobrevivente já marcado como infectado.')})
        else:
            survivor_infected.infected = True
            survivor_infected.save()
        return Response({'message': _('Sobrevivente marcado como infectado.')})
    return Response({'message': _('Operação não realizada. É preciso três sobreviventes únicos e o suspeito de estar infectado não pode ser quem acusa.')})

#continuar...
@api_view(['GET'])
def survivors_percent_infected_report(request):
    """
    Retorna o percentual de sobreviventes infectados.
    """
    survivors = Survivor.objects.all()
    infected_survivors = survivors.filter(infected=True)
    percents = infected_survivors.count() / survivors.count() * 100
    return Response({'survivors_percent_infected': '{0:.2f}'.format(percents)})


@api_view(['GET'])
def survivors_percent_not_infected_report(request):
    """
    Retorna o percentual de sobreviventes não infectados.
    """
    survivors = Survivor.objects.all()
    not_infected_survivors = survivors.filter(infected=False)
    percents = not_infected_survivors.count() / survivors.count() * 100
    return Response({'survivors_percent_not_infected': '{0:.2f}'.format(percents)})


@api_view(['GET'])
def average_item_by_survivors_report(request):
    """
    Retorna a média de itens por sobreviventes.
    """
    survivors = Survivor.objects.count()
    inventory = Inventory.objects.values('item__name').order_by('item').annotate(total_items=Sum('quantity'))
    print('inventory.all', inventory.all())
    report_data = []
    for i in inventory:
        report_data.append(
            {
                'item': i.get('item__name'),
                'survivor_average': '{0:.2f}'.format(i.get('total_items') / survivors)
            }
        )
    return Response(report_data)


@api_view(['GET'])
def points_lost_by_infected_survivors_report(request):
    """
    Retorna a quantidade de pontos perdidos por conta dos sobreviventes infectados.
    """
    infected_survivors = Survivor.objects.filter(infected=True)
    infected_survivors_list = []
    total_points_lost = 0
    for s in infected_survivors:
        infected_survivors_list.append(s.name)
        inventory = Inventory.objects.filter(survivor=s)
        for i in inventory:
            total_points_lost += i.item.points
    report_data = {
        'total_points_lost': total_points_lost,
        'infected_survivors': infected_survivors_list
    }
    return Response(report_data)