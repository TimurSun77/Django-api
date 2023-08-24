from rest_framework import serializers
from django.conf import settings

from core.abstract.serializers import AbstractSerializer 
from core.user.models import User


class UserSerializer (AbstractSerializer):
    posts_count = serializers.SerializerMethodField()
    #id = serializers.UUIDField (source='public_id', read_only=True, format='hex')
    #created = serializers.DateTimeField(read_only=True)
    #updated = serializers.DateTimeField(read_only=True)
    # метод для подсчета количества постов
    def get_posts_count(self, instance):
        return instance.post_set.all().count()
    
    # метод для обработкие default avatar
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['avatar']:
            representation['avatar'] = settings.DEFAULT_AVATAR_URL
            return representation
        #if settings.DEBUG:  # debug enabled for dev
        #    request = self.context.get('request')
        #    representation['avatar'] = request.build_absolute_uri(representation['avatar'])
        return representation
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'bio', 'avatar', 'is_active', 'created', 'updated', 'posts_count' ]
        read_only_filed = ['is_active']
