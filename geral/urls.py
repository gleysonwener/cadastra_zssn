from . import views
from django.urls import path

app_name = 'geral'





urlpatterns = [
    path('', views.index, name='index'),
    path('marca-infectado/', views.marca_infectado, name='marca_infectado'), #marca sobrevivente como infectado
    path('rel-porcentagem-infectados/', views.rel_porcentagem_infectados, name='rel_porcentagem_infectados'),
    path('rel-porcentagem-nao-infectados/', views.rel_porcentagem_nao_infectados, name='rel_porcentagem_nao_infectados'),
    path('rel-media-itens-sobreviventes/', views.rel_media_itens_sobreviventes, name='rel_media_itens_sobreviventes'),
    path('rel-pontos-perdidos/', views.rel_pontos_perdidos, name='rel_pontos_perdidos'),
    path('itens/', views.ItemListCreateAPIView.as_view(), name='itens'), # cadastra itens do sobrevivente
    path('sobreviventes/', views.SobreviventeListCreateAPIView.as_view(), name='sobreviventes'), # cadastra sobrevivente
    path('inventarios/', views.InventarioListCreateAPIView.as_view(), name='inventarios'), # inventario
    path('sobrevivente-local/<int:sobrevivente_id>/', views.SobreviventeLocalUpdate.as_view(), name='sobrevivente-local'), # atuaiza local do sobrevivente
    path('troca-itens/', views.troca_itens, name='troca_itens'), # troca itens entre sobreviventes
]