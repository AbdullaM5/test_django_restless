import uuid

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from restless.dj import DjangoResource
from restless.exceptions import BadRequest
from restless.preparers import FieldsPreparer


class AccountRegisterResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'email': 'email',
        'type': 'type'
    })

    def create(self, *args, **kwargs):
        user_model = get_user_model()

        email = self.data.get('email', '')
        password = self.data.get('password', '')
        _type = self.data.get('type', '')

        if email and password and _type:
            if user_model.objects.filter(email__exact=email).exists():
                raise BadRequest('{} already taken'.format(email))
            try:
                validate_email(email)
                validate_password(password)
            except ValidationError as e:
                raise BadRequest(e.__str__())
            return user_model.objects.create_user(
                email=email,
                password=password,
                type=_type,
                username=uuid.uuid4()
            )
        raise BadRequest('Email, password and type must be set')

    def is_authenticated(self):
        return True


class AccountLoginResource(DjangoResource):
    def create(self, *args, **kwargs):
        user = authenticate(request=self.request, email=self.data.get('email'), password=self.data.get('password'))
        if user:
            login(self.request, user)
            return {'status': 'ok'}
        else:
            raise BadRequest('Invalid email/password')

    def is_authenticated(self):
        return True


class AccountLogoutResource(DjangoResource):
    def create(self, *args, **kwargs):
        logout(self.request)
        return {'status': 'ok'}

    def is_authenticated(self):
        return self.request.user.is_authenticated()
