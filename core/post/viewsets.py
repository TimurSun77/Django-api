#from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerialaizer
from core.auth.permissions import UserPermission

class PostViewSet (AbstractViewSet):
    http_method_names=('post', 'get', 'put', 'delete') #разрешаем только эти методы в API
    permission_classes=(UserPermission,) #авторизация берется из класса UserPermission
    serializer_class=PostSerialaizer # указваем, что сериалйзер используется из post.serializers
    filterset_fields = ['author__public_id']# создаем фильтры ВНИМАНИЕ тут два нижних подчеркивания (__) таким образом мы говорим author и publicId автора

    def get_queryset(self): #этот метод возвращает все посты
        return Post.objects.all()
    
    def get_object(self): # этот метод возвращает объект Post используя public_id который будет в URL (который мы получим из директории self.kwargs)
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        
        return obj
    # собствено метод создания поста который происходит по запросу POST
    def create(self,request, *args, **swargs):
        serializer=self.get_serializer(data=request.data) #передаем даные в сериалайзер
        serializer.is_valid(raise_exception=True) #проводим валидацию данных на соответствие требованиям Модели
        self.perform_create(serializer) #создаем объект post
        return Response(serializer.data, status=status.HTTP_201_CREATED) #возвращаем ответ с данными из только-что созданного поста
   
    @action(methods=['post'], detail=True)
    def like (self, request, *args, **kwargs):
        post=self.get_object() # вернет именно пост которому ставим лайк
        user=self.request.user  # получаем пользователя из запроса

        user.like(post) # вызываем метод like из модели User
        serializer = self.serializer_class(post) # запускаем сериалайзер для подготовки ответа
        return Response(serializer.data, status=status.HTTP_200_OK) #возвращаем ответ
    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post=self.get_object() # возвращает пост над которым нужно произвести действия
        user=self.request.user # получаем пользователя из запроса

        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
