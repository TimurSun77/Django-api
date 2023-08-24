from rest_framework import viewsets
#from rest_framework import filters

class AbstractViewSet(viewsets.ModelViewSet):
    #filter_backends = [filters.OrderingFilter] # устанавливает фильтр по умолчанию
    ordering_fields=['updated', 'created'] # список полей которые могут быть использованы для уопрядочивания
    ordering = ['-updated'] # устанвливает порядок упорядочивания - самый последний обновленный пост