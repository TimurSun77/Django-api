#import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#from django.core.exceptions import ObjectDoesNotExist
from django.db import models
#from django.http import Http404
from core.abstract.models import AbstractManager, AbstractModel # импортируем классы из abstract 
# функция 
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.public_id, filename)


# Добывим в этот класс также функционал AbstractManager
class UserManager(BaseUserManager, AbstractManager): 
    # закомитили эту функцию, так как передали ее действия в abstract сабкласс
    # def get_object_by_public_id(self, public_id):
    #    try:
    #        instance = self.get(public_id=public_id)
    #        return instance
    #    except  (ObjectDoesNotExist, ValueError, TypeError):
    #        return Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a 'User' with an email, phone number, username and password"""
        if username is None:
            raise TypeError('Users must have an username')
        if email is None:
            raise TypeError('Users must have an email')
        if password is None:
            raise TypeError('Users must have a password')
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self,username, email, password, **kwargs):
        """Create and return a 'User' with superuser (admin) permissions."""
        if username is None:
            raise TypeError("Superusers must have an username.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if password is None:
            raise TypeError("Superusers must have a password.")
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff=True
        user.save(using=self._db)

        return user 
# Добавим в этот класс такдже функционал  AbstractModel из импортированного класса abstract
class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    #далее закомитины поля, которые были переданы в abstract (public_id, created, updated)
    #public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email=models.EmailField(db_index=True, unique=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    
    post_liked = models.ManyToManyField (
        "core_post.Post",
        related_name="liked_by"
    )
    comment_liked = models.ManyToManyField (
        "core_comment.Comment",
        related_name="commen_liked_by"
    )
    #created = models.DateTimeField(auto_now=True)
    #updated=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()

    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    def like(self, post):
        """Like 'post' if it hasn't been done yet"""
        return self.post_liked.add(post)
    def remove_like(self, post):
        """Remove a like from a post"""
        return self.post_liked.remove(post)
    def has_liked(self, post):
        """Return True if the user liked a 'post' else retrun False"""
        return self.post_liked.filter(pk=post.pk).exists()
    
    def like_comment(self, comment):
        """Like `comment` if it hasn't been done yet"""
        return self.comment_liked.add(comment)
    
    def remove_like_comment(self, comment):
        """Remove a like from a `comment`"""
        return self.comment_liked.remove(comment)
    
    def has_liked_comment(self, comment):
        """Return True if the user has liked a `comment`; else False"""
        return self.comment_liked.filter(pk=comment.pk).exists()

