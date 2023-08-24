from django.test import TestCase
import pytest
from core.user.models import User

# данные пользователя
data_user = {
    "username": "test_user",
    "email": "test@gamil.com",
    "first_name":"Test",
    "last_name": "User",
    "password": "test_password"
}
#пишем функции тестирования
@pytest.mark.django_db # декоратор для достпуа к базе django
def test_create_user(): #тестирование создания пользователя
    user = User.objects.create_user(**data_user)
    assert user.username == data_user["username"]
    assert user.email == data_user["email"]
    assert user.first_name == data_user["first_name"]
    assert user.last_name == data_user["last_name"]
# данные суперпользователья    
data_superuser ={
    "username": "test",
    "email": "testsuperuser@gmail.com",
    "first_name": "Test",
    "last_name": "Superuser",
    "password":"test_password"
}
@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(**data_superuser)
    assert user.username == data_superuser["username"]
    assert user.email == data_superuser["email"]
    assert user.first_name == data_superuser["first_name"]
    assert user.last_name == data_superuser["last_name"]
    assert user.is_superuser == True
    assert user.is_staff == True

