from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
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


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('Nome', max_length=255)
    email = models.EmailField('Email', max_length=255, unique=True)
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
