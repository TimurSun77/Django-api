from django.http.response import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action # для использования спец декторатора


from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes=(UserPermission,)
    serializer_class=CommentSerializer
    # метод который вызывается если пользователь запросит /api/ post/post_pk/comment/
    def get_queryset(self):
        if self.request.user.is_superuser: #если пользователь суперпользователь, 
            return Comment.objects.all()   # то все комменты загружаем
        # так-как в nested route для POST мы прописали lookup='post' 
        # то для каждого запроса должен приходить дополнительный kwargs словарь, с ключом post_pk значение public_id поста
        post_pk = self.kwargs['post_pk'] #определяем пост к которому относится коммент  
        if post_pk is None: # если дополнительного словаря не пришло
            return Http404 # то возвращаем 404 Not Found ответ
        queryset = Comment.objects.filter(post__public_id=post_pk) #запрос в базу на коменты с фильтром post.public_id=post_pk

        return queryset
    # метов для получения коментов по pubplic_id - /api/post/post_pk/comment/comment_pk/
    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs['pk']) # здесь pk относится к таблице comment_pk

        self.check_object_permissions(self.request, obj) # проверям правила доступа

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # весь этот блок далее для обработки лайков на комменты
    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        comment = self.get_object()
        user = self.request.user

        user.like_comment(comment)

        serializer = self.serializer_class(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        comment = self.get_object()
        user = self.request.user

        user.remove_like_comment(comment)

        serializer = self.serializer_class(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # это было в книге, но при этом не работает
    #def update (self, instance, validate_data):
    #    if not instance.edited:
    #        validate_data['edited']=True
    #    instance = super().update(instance, validate_data)
    #    return instance