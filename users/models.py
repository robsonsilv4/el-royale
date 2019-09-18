from uuid import uuid4

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import EmailValidator
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('O email é obrigatório.')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField('Nome', max_length=255)
    email = models.EmailField('Email', max_length=255,
                              unique=True, validators=[EmailValidator(message='Email inválido.'), ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def get_full_name(self):
        return self.name

    def get_shot_name(self):
        return self.name

    def __str__(self):
        return self.name
