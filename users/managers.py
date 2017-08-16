from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, type, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        if not type:
            raise ValueError('Type must be set')
        user = self.model(email=self.normalize_email(email=email), type=type, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, type, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, type=type, **extra_fields)

    def create_superuser(self, email, password, type, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, password=password, type=type, **extra_fields)
